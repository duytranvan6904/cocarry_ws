import json

def add_md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [line + "\n" for line in text.split('\n')]})

def add_code(text):
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" for line in text.split('\n')]})

cells = []

add_md("# Autoregressive Hyperparameter Tuning\n\nSử dụng KerasTuner để tìm tổ hợp siêu tham số tối ưu nhất cho model Autoregressive.")

code1 = """!pip install keras-tuner -q
import numpy as np
import pandas as pd
import os
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GRU, Dense, Input, Lambda, Reshape, Concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import keras_tuner as kt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# ===== CẤU HÌNH =====
T = 20               # Input history length
H = 8                # Prediction horizon (0.5s ở 16Hz)
PRED_STEPS = 171
SEQUENCE_LENGTH = T + PRED_STEPS  # = 191
EPOCHS = 80

def set_seed(seed=42):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

set_seed(42)

# ===== AUTO-DETECT COLAB vs LOCAL =====
try:
    from google.colab import drive
    IN_COLAB = True
    drive.mount('/content/drive')
    BASE_PATH = '/content/drive/MyDrive/GRU-Model/'
except ImportError:
    IN_COLAB = False
    BASE_PATH = '.'

TRAIN_DATA_PATH = os.path.join(BASE_PATH, 'train_trajectories.csv')
TEST_DATA_PATH  = os.path.join(BASE_PATH, 'test_trajectories.csv')
"""
add_code(code1)

add_md("## Tiền xử lý dữ liệu (Load & Scale)")

code2 = """def load_data(file_path):
    if not os.path.exists(file_path): raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path)
    return df[['x', 'y', 'z']].values if 'x' in df.columns else df[['X', 'Y', 'Z']].values

def create_data_multistep_sequence(data, T, H, sequence_length):
    X, y = [], []
    num_trajectories = len(data) // sequence_length
    for i in range(num_trajectories):
        trajectory = data[i*sequence_length : (i+1)*sequence_length]
        if trajectory.shape != (sequence_length, 3): continue
        velocity = np.zeros_like(trajectory)
        velocity[1:] = trajectory[1:] - trajectory[:-1]
        velocity[0] = 0
        traj_features = np.hstack([trajectory, velocity])
        
        for j in range(sequence_length - H + 1):
            if j < T:
                num_zeros = T - j
                zero_padding = np.zeros((num_zeros, 6))
                if j > 0:
                    real_points = traj_features[0:j]
                    input_sequence = np.vstack([zero_padding, real_points])
                else:
                    input_sequence = zero_padding
            else:
                input_sequence = traj_features[j-T:j]
                
            output_sequence = trajectory[j : j + H]
            X.append(input_sequence)
            y.append(output_sequence)
    return np.array(X), np.array(y)

def fit_scalers(X, y):
    scaler_x = {'x': MinMaxScaler(), 'y': MinMaxScaler(), 'z': MinMaxScaler(), 'vx': MinMaxScaler(), 'vy': MinMaxScaler(), 'vz': MinMaxScaler()}
    scaler_y = {'x': MinMaxScaler(), 'y': MinMaxScaler(), 'z': MinMaxScaler()}
    
    for i, key in enumerate(['x', 'y', 'z', 'vx', 'vy', 'vz']):
        scaler_x[key].fit(X[:, :, i].reshape(-1, 1))
    for i, key in enumerate(['x', 'y', 'z']):
        scaler_y[key].fit(y[:, :, i].reshape(-1, 1))
    return scaler_x, scaler_y

def transform_data(X, y, scaler_x, scaler_y):
    num_samples_x, T_steps, _ = X.shape
    X_scaled = np.zeros_like(X)
    for i, key in enumerate(['x', 'y', 'z', 'vx', 'vy', 'vz']):
        X_scaled[:, :, i] = scaler_x[key].transform(X[:, :, i].reshape(-1, 1)).reshape(num_samples_x, T_steps)
        
    y_scaled = None
    if y is not None:
        num_samples_y, H_steps, _ = y.shape
        y_scaled = np.zeros_like(y)
        for i, key in enumerate(['x', 'y', 'z']):
            y_scaled[:, :, i] = scaler_y[key].transform(y[:, :, i].reshape(-1, 1)).reshape(num_samples_y, H_steps)
    return X_scaled, y_scaled

def inverse_transform_y(y_scaled, scaler_y):
    num_samples_y, H_steps, _ = y_scaled.shape
    y_orig = np.zeros_like(y_scaled)
    for i, key in enumerate(['x', 'y', 'z']):
        y_orig[:, :, i] = scaler_y[key].inverse_transform(y_scaled[:, :, i].reshape(-1, 1)).reshape(num_samples_y, H_steps)
    return y_orig

# Load data
print("Đang tải dữ liệu...")
raw_train = load_data(TRAIN_DATA_PATH)
raw_test = load_data(TEST_DATA_PATH)

print(f"Đang tạo sequence (H={H})...")
X_train_raw, y_train_raw = create_data_multistep_sequence(raw_train, T, H, SEQUENCE_LENGTH)
X_test_raw, y_test_raw = create_data_multistep_sequence(raw_test, T, H, SEQUENCE_LENGTH)

indices = np.arange(len(X_train_raw))
idx_train, idx_val = train_test_split(indices, test_size=0.1765, random_state=42, shuffle=True)

X_train, y_train = X_train_raw[idx_train], y_train_raw[idx_train]
X_val, y_val = X_train_raw[idx_val], y_train_raw[idx_val]
X_test, y_test = X_test_raw, y_test_raw

print("Fitting scalers...")
scaler_x, scaler_y = fit_scalers(X_train, y_train)

X_train_s, y_train_s = transform_data(X_train, y_train, scaler_x, scaler_y)
X_val_s, y_val_s = transform_data(X_val, y_val, scaler_x, scaler_y)
X_test_s, y_test_s = transform_data(X_test, y_test, scaler_x, scaler_y)
"""
add_code(code2)

add_md("## Thiết lập KerasTuner cho Autoregressive Model\nCấu hình `num_layers` từ 1-5, `gru_units` [64, 128, 256], `dropout` [0.1, 0.2].")

code3 = """class AutoregressiveHyperModel(kt.HyperModel):
    def __init__(self, input_shape, H):
        self.input_shape_ = input_shape
        self.H = H

    def build(self, hp):
        gru_units = hp.Choice('gru_units', values=[64, 128, 256])
        dropout_rate = hp.Choice('dropout_rate', values=[0.1, 0.2])
        num_layers = hp.Int('num_layers', min_value=1, max_value=5, step=1)
        # Learning rate cố định 0.001 theo yêu cầu
        learning_rate = 0.001 
        
        inputs = Input(shape=self.input_shape_, name='input_sequence')
        
        # --- ENCODER ---
        x = inputs
        states = []
        for i in range(num_layers):
            return_seq = (i < num_layers - 1)
            encoder_gru = GRU(
                gru_units, 
                activation='tanh', 
                return_sequences=return_seq, 
                return_state=True,
                dropout=dropout_rate,
                name=f'encoder_gru_{i}'
            )
            
            if return_seq:
                x, state_h = encoder_gru(x)
            else:
                _, state_h = encoder_gru(x)
            states.append(state_h)
            
        # --- DECODER CELLS ---
        cells = []
        for i in range(num_layers):
            cells.append(tf.keras.layers.GRUCell(
                gru_units, 
                activation='tanh', 
                name=f'decoder_gru_cell_{i}'
            ))
            
        if num_layers > 1:
            stacked_cells = tf.keras.layers.StackedRNNCells(cells, name='stacked_decoder_cells')
        else:
            stacked_cells = cells[0]
            
        decoder_dropout = tf.keras.layers.Dropout(dropout_rate, name='decoder_dropout')
        dense_out = Dense(3, name='dense_projection')
        
        # Trích xuất vị trí cuối cùng của chuỗi lịch sử làm mốc
        last_pos = Lambda(lambda x: x[:, -1, :3], output_shape=(3,), name='extract_last_pos')(inputs)
        
        outputs = []
        current_state = states
        current_input = last_pos
        
        for h in range(self.H):
            x, current_state = stacked_cells(current_input, states=current_state)
            x = decoder_dropout(x)
            pred = dense_out(x)
            pred_reshaped = Reshape((1, 3))(pred)
            outputs.append(pred_reshaped)
            current_input = pred
            
        out_tensor = Concatenate(axis=1, name='concat_outputs')(outputs)
        
        model = Model(inputs=inputs, outputs=out_tensor, name="Tuned_Autoregressive")
        model.compile(optimizer=Adam(learning_rate), loss='mse', metrics=['mae'])
        return model

    def fit(self, hp, model, *args, **kwargs):
        # KerasTuner cho phép tune luôn cả batch_size
        batch_size = hp.Choice('batch_size', values=[32, 64])
        return model.fit(
            *args,
            batch_size=batch_size,
            **kwargs
        )
"""
add_code(code3)

add_md("## Chạy quá trình Tuning (Hyperband)")

code4 = """print("Khởi tạo KerasTuner Hyperband...")
hypermodel = AutoregressiveHyperModel(input_shape=(T, 6), H=H)

tuner = kt.Hyperband(
    hypermodel,
    objective='val_loss',
    max_epochs=80,
    factor=3,
    directory=BASE_PATH,
    project_name='autoregressive_tuning',
    overwrite=False # Đổi thành True nếu muốn reset tuning từ đầu
)

tuner.search_space_summary()

early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6)

print("\\nBắt đầu tìm kiếm tham số tối ưu...")
tuner.search(
    X_train_s, y_train_s,
    epochs=EPOCHS,
    validation_data=(X_val_s, y_val_s),
    callbacks=[early_stop, reduce_lr],
    verbose=1
)

# Lấy ra bộ tham số tốt nhất
best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

print("\\n" + "="*50)
print("THÔNG SỐ TỐI ƯU NHẤT TÌM ĐƯỢC:")
print(f"Số lớp (num_layers): {best_hps.get('num_layers')}")
print(f"Số node GRU (gru_units): {best_hps.get('gru_units')}")
print(f"Dropout Rate: {best_hps.get('dropout_rate')}")
print(f"Batch Size: {best_hps.get('batch_size')}")
print("="*50)
"""
add_code(code4)

add_md("## Đánh giá Model Tốt nhất (ADE & FDE)")

code5 = """# Lấy ra mô hình tốt nhất
best_model = tuner.get_best_models(num_models=1)[0]

# Đánh giá trên tập Test
y_pred_scaled = best_model.predict(X_test_s, batch_size=256, verbose=0)
y_pred_orig = inverse_transform_y(y_pred_scaled, scaler_y)
y_test_orig = inverse_transform_y(y_test_s, scaler_y)

fde = np.mean(np.sqrt(np.sum((y_pred_orig[:, -1, :] - y_test_orig[:, -1, :]) ** 2, axis=1)))
ade = np.mean([
    np.mean(np.sqrt(np.sum((y_pred_orig[i] - y_test_orig[i]) ** 2, axis=1)))
    for i in range(len(y_test_orig))
])

print(f"Best Model Test ADE: {ade:.5f} m")
print(f"Best Model Test FDE: {fde:.5f} m")

# Lưu mô hình xuất sắc nhất
best_model_path = os.path.join(BASE_PATH, 'Best_Autoregressive.keras')
best_model.save(best_model_path)
print(f"Đã lưu mô hình tốt nhất tại: {best_model_path}")
"""
add_code(code5)

notebook = {
    "cells": cells,
    "metadata": {
        "colab": {
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open("Autoregressive_Tuning.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Tuning Notebook generated successfully.")
