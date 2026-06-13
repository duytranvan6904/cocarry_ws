import json
import os

nb = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

def add_md(text):
    source = [line + "\\n" for line in text.split("\\n")]
    # remove trailing newline of the last element
    if len(source) > 0 and source[-1].endswith("\\n"):
        source[-1] = source[-1][:-1]
    nb["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    })

def add_code(text):
    source = [line + "\\n" for line in text.split("\\n")]
    if len(source) > 0 and source[-1].endswith("\\n"):
        source[-1] = source[-1][:-1]
    nb["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    })

md1 = """# Multi-Step Trajectory Prediction (t+1 to t+H)

Notebook này thực hiện dự đoán một chuỗi điểm tương lai (multi-step prediction) dựa trên lịch sử T bước để hỗ trợ MPC controller bù trễ.
Bao gồm 3 phương án kiến trúc:
1. **Direct Multi-Output**: Dự đoán H điểm đồng thời thông qua 1 Dense layer.
2. **Seq2Seq Encoder-Decoder**: Sử dụng Decoder GRU để giải mã và dự đoán tuần tự H bước.
3. **Autoregressive**: Sử dụng chính dự đoán của t+1 để dự đoán t+2, v.v..."""
add_md(md1)

add_md("## 1. Cấu hình và Thiết lập Môi trường")

code1 = """import numpy as np
import pandas as pd
import pickle
import time
import os
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GRU, LSTM, SimpleRNN, Dense, Dropout, Input, RepeatVector, TimeDistributed, Lambda
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# ===== CẤU HÌNH =====
T = 20               # Input history length
H = 8                # Prediction horizon (0.5s ở 16Hz)
NUM_FEATURES = 6     # x, y, z, vx, vy, vz
PRED_STEPS = 171     # Số bước dự đoán mỗi quỹ đạo (chứa điểm tương lai xa nhất)
SEQUENCE_LENGTH = T + PRED_STEPS  # = 191
SAMPLING_FREQ = 16   # Hz
BATCH_SIZE = 64
EPOCHS = 80
NUM_RUNS = 1         # Số lần chạy mỗi model để lấy trung bình

def set_seed(seed=42):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

# ===== AUTO-DETECT COLAB vs LOCAL =====
try:
    from google.colab import drive
    IN_COLAB = True
    drive.mount('/content/drive')
    BASE_PATH = '/content/drive/MyDrive/GRU-Model/'
except ImportError:
    IN_COLAB = False
    BASE_PATH = '.'  # Đường dẫn local

TRAIN_DATA_PATH = os.path.join(BASE_PATH, 'train_trajectories.csv')
TEST_DATA_PATH  = os.path.join(BASE_PATH, 'test_trajectories.csv')"""
add_code(code1)

add_md("## 2. Load và Tiền xử lý dữ liệu\nSử dụng `create_data_multistep_sequence()` để tạo chuỗi H điểm dự đoán.")

code2 = """def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path)
    return df[['x', 'y', 'z']].values if 'x' in df.columns else df[['X', 'Y', 'Z']].values

def create_data_multistep_sequence(data, T, H, sequence_length):
    X, y = [], []
    num_trajectories = len(data) // sequence_length
    print(f"Số lượng quỹ đạo: {num_trajectories}")
    for i in range(num_trajectories):
        trajectory = data[i*sequence_length : (i+1)*sequence_length]
        if trajectory.shape != (sequence_length, 3): continue
        velocity = np.zeros_like(trajectory)
        velocity[1:] = trajectory[1:] - trajectory[:-1]
        velocity[0] = 0
        traj_features = np.hstack([trajectory, velocity])
        
        # Chúng ta slide window
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
    
    scaler_x['x'].fit(X[:, :, 0].reshape(-1, 1))
    scaler_x['y'].fit(X[:, :, 1].reshape(-1, 1))
    scaler_x['z'].fit(X[:, :, 2].reshape(-1, 1))
    scaler_x['vx'].fit(X[:, :, 3].reshape(-1, 1))
    scaler_x['vy'].fit(X[:, :, 4].reshape(-1, 1))
    scaler_x['vz'].fit(X[:, :, 5].reshape(-1, 1))
    
    scaler_y['x'].fit(y[:, :, 0].reshape(-1, 1))
    scaler_y['y'].fit(y[:, :, 1].reshape(-1, 1))
    scaler_y['z'].fit(y[:, :, 2].reshape(-1, 1))
    return scaler_x, scaler_y

def transform_data(X, y, scaler_x, scaler_y):
    num_samples, T, _ = X.shape
    X_scaled = np.zeros_like(X)
    X_scaled[:, :, 0] = scaler_x['x'].transform(X[:, :, 0].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 1] = scaler_x['y'].transform(X[:, :, 1].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 2] = scaler_x['z'].transform(X[:, :, 2].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 3] = scaler_x['vx'].transform(X[:, :, 3].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 4] = scaler_x['vy'].transform(X[:, :, 4].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 5] = scaler_x['vz'].transform(X[:, :, 5].reshape(-1, 1)).reshape(num_samples, T)
    
    y_scaled = None
    if y is not None:
        num_samples_y, H, _ = y.shape
        y_scaled = np.zeros_like(y)
        y_scaled[:, :, 0] = scaler_y['x'].transform(y[:, :, 0].reshape(-1, 1)).reshape(num_samples_y, H)
        y_scaled[:, :, 1] = scaler_y['y'].transform(y[:, :, 1].reshape(-1, 1)).reshape(num_samples_y, H)
        y_scaled[:, :, 2] = scaler_y['z'].transform(y[:, :, 2].reshape(-1, 1)).reshape(num_samples_y, H)
        
    return X_scaled, y_scaled

def inverse_transform_y(y_scaled, scaler_y):
    num_samples_y, H, _ = y_scaled.shape
    y_orig = np.zeros_like(y_scaled)
    y_orig[:, :, 0] = scaler_y['x'].inverse_transform(y_scaled[:, :, 0].reshape(-1, 1)).reshape(num_samples_y, H)
    y_orig[:, :, 1] = scaler_y['y'].inverse_transform(y_scaled[:, :, 1].reshape(-1, 1)).reshape(num_samples_y, H)
    y_orig[:, :, 2] = scaler_y['z'].inverse_transform(y_scaled[:, :, 2].reshape(-1, 1)).reshape(num_samples_y, H)
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

print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
print(f"X_val: {X_val.shape}, y_val: {y_val.shape}")
print(f"X_test: {X_test.shape}, y_test: {y_test.shape}")

print("Fitting scalers...")
scaler_x, scaler_y = fit_scalers(X_train, y_train)

X_train_s, y_train_s = transform_data(X_train, y_train, scaler_x, scaler_y)
X_val_s, y_val_s = transform_data(X_val, y_val, scaler_x, scaler_y)
X_test_s, y_test_s = transform_data(X_test, y_test, scaler_x, scaler_y)
"""
add_code(code2)

add_md("## 3. Xây dựng 3 Kiến trúc Model Multi-Step")

code3 = """def build_direct_model(input_shape, H):
    inputs = Input(shape=input_shape, name='input_sequence')
    x = GRU(128, activation='tanh', return_sequences=False)(inputs)
    x = Dropout(0.2)(x)
    x = Dense(H * 3)(x)
    outputs = tf.keras.layers.Reshape((H, 3), name='position_output')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name="Direct_MultiOutput")
    model.compile(optimizer=Adam(0.001), loss='mse', metrics=['mae'])
    return model

def build_seq2seq_model(input_shape, H):
    inputs = Input(shape=input_shape, name='input_sequence')
    
    encoder_gru = GRU(128, activation='tanh', return_state=True)
    encoder_outputs, state_h = encoder_gru(inputs)
    
    repeat_state = RepeatVector(H)(state_h)
    
    decoder_gru = GRU(128, activation='tanh', return_sequences=True)
    decoder_outputs = decoder_gru(repeat_state, initial_state=state_h)
    decoder_outputs = Dropout(0.2)(decoder_outputs)
    
    outputs = TimeDistributed(Dense(3))(decoder_outputs)
    
    model = Model(inputs=inputs, outputs=outputs, name="Seq2Seq")
    model.compile(optimizer=Adam(0.001), loss='mse', metrics=['mae'])
    return model

def build_autoregressive_model(input_shape, H):
    inputs = Input(shape=input_shape, name='input_sequence')
    
    encoder_gru = GRU(128, activation='tanh', return_state=True)
    _, state_h = encoder_gru(inputs)
    
    gru_cell = tf.keras.layers.GRUCell(128, activation='tanh')
    dense_out = Dense(3)
    
    # Thêm output_shape để tránh lỗi khi load_model
    last_pos = Lambda(lambda x: x[:, -1, :3], output_shape=(3,), name='extract_last_pos')(inputs)
    
    outputs = []
    current_state = [state_h]
    current_input = last_pos
    
    for h in range(H):
        x, current_state = gru_cell(current_input, states=current_state)
        pred = dense_out(x)
        # Reshape pred từ (batch, 3) thành (batch, 1, 3) để chuẩn bị Concatenate
        pred_reshaped = tf.keras.layers.Reshape((1, 3))(pred)
        outputs.append(pred_reshaped)
        current_input = pred
        
    # Sử dụng Concatenate thay cho Lambda tf.stack để tương thích tốt hơn khi save/load
    out_tensor = tf.keras.layers.Concatenate(axis=1, name='concat_outputs')(outputs)
    
    model = Model(inputs=inputs, outputs=out_tensor, name="Autoregressive")
    model.compile(optimizer=Adam(0.001), loss='mse', metrics=['mae'])
    return model

def get_model_size(model):
    temp_path = 'temp_model.keras'
    model.save(temp_path)
    size_mb = os.path.getsize(temp_path) / (1024 * 1024)
    if os.path.exists(temp_path): os.remove(temp_path)
    return size_mb
"""
add_code(code3)

add_md("## 4. Pipeline Training & Ablation")

code4 = """def run_multistep_study(X_train, y_train, X_val, y_val, X_test, y_test, H, epochs=80, batch_size=64, num_runs=1):
    input_shape = (X_train.shape[1], X_train.shape[2])
    
    configs = [
        {'name': 'Direct_MultiOutput', 'builder': build_direct_model},
        {'name': 'Seq2Seq', 'builder': build_seq2seq_model},
        {'name': 'Autoregressive', 'builder': build_autoregressive_model}
    ]
    
    results = []
    models_dict = {}
    histories_dict = {}

    for config in configs:
        name = config['name']
        builder = config['builder']
        
        print(f"\\n{'='*80}")
        print(f"CONFIGURATION: {name}")
        print(f"{'='*80}")
        
        run_metrics = {
            'test_loss': [], 'test_mae': [],
            'best_val_loss': [], 'best_val_mae': [],
            'training_time': [], 'inference_time': []
        }
        
        for run in range(num_runs):
            set_seed(42 + run)
            model = builder(input_shape, H)
            
            if run == 0:
                total_params = model.count_params()
                
            early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True, verbose=0)
            reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6, verbose=0)
            
            start_time = time.time()
            history = model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                epochs=epochs,
                batch_size=batch_size,
                callbacks=[early_stop, reduce_lr],
                verbose=1
            )
            training_time = time.time() - start_time
            
            eval_results = model.evaluate(X_test, y_test, verbose=0, batch_size=batch_size)
            test_loss, test_mae = eval_results[0], eval_results[1]
            
            test_samples = X_test[:100]
            if len(test_samples) > 0:
                _ = model.predict(test_samples[0:1], verbose=0)
                infer_start = time.time()
                for i in range(len(test_samples)):
                    _ = model.predict(test_samples[i:i+1], verbose=0)
                inference_time = (time.time() - infer_start) / len(test_samples) * 1000
            else:
                inference_time = 0
                
            run_metrics['test_loss'].append(test_loss)
            run_metrics['test_mae'].append(test_mae)
            
            val_loss_hist = history.history['val_loss']
            best_epoch_idx = np.argmin(val_loss_hist)
            run_metrics['best_val_loss'].append(val_loss_hist[best_epoch_idx])
            run_metrics['best_val_mae'].append(history.history['val_mae'][best_epoch_idx])
            run_metrics['training_time'].append(training_time)
            run_metrics['inference_time'].append(inference_time)
            
            if run == num_runs - 1:
                models_dict[name] = model
                histories_dict[name] = history
                
        avg_result = {
            'name': name,
            'total_params': total_params,
            'test_loss': np.mean(run_metrics['test_loss']),
            'test_mae': np.mean(run_metrics['test_mae']),
            'val_loss': np.mean(run_metrics['best_val_loss']),
            'val_mae': np.mean(run_metrics['best_val_mae']),
            'training_time_s': np.mean(run_metrics['training_time']),
            'inference_time_ms': np.mean(run_metrics['inference_time']),
            'model_size_mb': get_model_size(model)
        }
        results.append(avg_result)
        print(f"AVG RESULT ({name}):")
        print(f"   Test Loss: {avg_result['test_loss']:.6f}, MAE: {avg_result['test_mae']:.6f}")
        print(f"   Val Loss:  {avg_result['val_loss']:.6f}, MAE: {avg_result['val_mae']:.6f}")
        
    return pd.DataFrame(results), models_dict, histories_dict

print("Bắt đầu training 3 phương án Multi-Step...")
results_df, models_dict, histories_dict = run_multistep_study(X_train_s, y_train_s, X_val_s, y_val_s, X_test_s, y_test_s, H, epochs=EPOCHS, batch_size=BATCH_SIZE, num_runs=NUM_RUNS)
"""
add_code(code4)

add_md("### 4.1 Save Trained Models\n\nLưu các model đã huấn luyện lên Google Drive để tái sử dụng.")

code4_save = """import os

print(f"Current models in memory: {list(models_dict.keys())}")
print("Saving trained models to Google Drive...")

if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

if not models_dict:
    print("WARNING: models_dict is empty. Nothing to save. Please run the training cell first.")
else:
    for name, model in models_dict.items():
        save_path = os.path.join(BASE_PATH, f'{name}.keras')
        try:
            model.save(save_path)
            print(f"Successfully saved {name} model to {save_path}")
        except Exception as e:
            print(f"Error saving {name} model to {save_path}: {e}")

    print(f"Model saving process complete. Total models processed: {len(models_dict)}")
"""
add_code(code4_save)

add_md("### 4.2 Load Pre-trained Models (Alternative to training)\n\nNếu bạn đã train model trước đó, có thể load lại tại đây thay vì chạy lại pipeline training.")

code4_load = """import os
import tensorflow as tf

models_dict = {}
model_names = ['Direct_MultiOutput', 'Seq2Seq', 'Autoregressive']

print("Attempting to load pre-trained models from Drive...")
for name in model_names:
    model_path = os.path.join(BASE_PATH, f'{name}.keras')
    if os.path.exists(model_path):
        try:
            models_dict[name] = tf.keras.models.load_model(model_path, compile=True, safe_mode=False)
            print(f"[SUCCESS] Loaded {name} model.")
        except Exception as e:
            print(f"[ERROR] Could not load {name}: {e}")
    else:
        print(f"[NOT FOUND] {model_path}")

if len(models_dict) == len(model_names):
    print("\\nAll models loaded successfully!")
else:
    print(f"\\nLoaded {len(models_dict)}/{len(model_names)} models.")
"""
add_code(code4_load)

add_md("## 5. Đánh giá Định lượng (ADE, FDE, Error vs Horizon)")

code5 = """def evaluate_ade_fde(models_dict, X_test, y_test, scaler_y):
    metrics = []
    y_test_orig = inverse_transform_y(y_test, scaler_y)
    
    for name, model in models_dict.items():
        y_pred_scaled = model.predict(X_test, batch_size=256, verbose=0)
        y_pred_orig = inverse_transform_y(y_pred_scaled, scaler_y)
        
        fde = np.mean(np.sqrt(np.sum((y_pred_orig[:, -1, :] - y_test_orig[:, -1, :]) ** 2, axis=1)))
        ade = np.mean([
            np.mean(np.sqrt(np.sum((y_pred_orig[i] - y_test_orig[i]) ** 2, axis=1)))
            for i in range(len(y_test_orig))
        ])
        
        metrics.append({
            'Model': name,
            'ADE (m)': ade,
            'FDE (m)': fde
        })
        
    return pd.DataFrame(metrics)

print("Đánh giá ADE, FDE trên tập test (đơn vị: mét):")
ade_fde_df = evaluate_ade_fde(models_dict, X_test_s, y_test_s, scaler_y)
print(ade_fde_df.to_string())

def plot_error_vs_horizon(models_dict, X_test, y_test, scaler_y, H):
    y_test_orig = inverse_transform_y(y_test, scaler_y)
    
    plt.figure(figsize=(10, 6))
    for name, model in models_dict.items():
        y_pred_scaled = model.predict(X_test, batch_size=256, verbose=0)
        y_pred_orig = inverse_transform_y(y_pred_scaled, scaler_y)
        
        errors = []
        for h in range(H):
            mse_h = np.mean((y_pred_orig[:, h, :] - y_test_orig[:, h, :]) ** 2)
            rmse_h = np.sqrt(mse_h)
            errors.append(rmse_h)
            
        plt.plot(range(1, H+1), errors, marker='o', label=name)
        
    plt.xlabel('Prediction Step (h)')
    plt.ylabel('RMSE (m)')
    plt.title(f'Error vs Prediction Horizon (H={H})')
    plt.grid(True)
    plt.legend()
    plt.show()

plot_error_vs_horizon(models_dict, X_test_s, y_test_s, scaler_y, H)
"""
add_code(code5)

add_md("## 6. Đánh giá Định tính (Visualize 3D và 2D)")

code6 = """def plot_3d_trajectory_comparison(model, X_test, y_test, scaler_x, scaler_y, sample_idx=0):
    X_sample_scaled = X_test[sample_idx:sample_idx+1]
    y_true_scaled = y_test[sample_idx:sample_idx+1]
    y_pred_scaled = model.predict(X_sample_scaled, verbose=0)
    
    history = scaler_x['x'].inverse_transform(X_sample_scaled[:, :, 0].reshape(-1,1)).ravel()
    history_y = scaler_x['y'].inverse_transform(X_sample_scaled[:, :, 1].reshape(-1,1)).ravel()
    history_z = scaler_x['z'].inverse_transform(X_sample_scaled[:, :, 2].reshape(-1,1)).ravel()
    
    y_true_orig = inverse_transform_y(y_true_scaled, scaler_y)[0]
    y_pred_orig = inverse_transform_y(y_pred_scaled, scaler_y)[0]
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(history, history_y, history_z, label='History (T steps)', color='gray', linestyle=':')
    ax.scatter(history[-1], history_y[-1], history_z[-1], color='black', label='Current Position')
    
    true_x = np.insert(y_true_orig[:, 0], 0, history[-1])
    true_y = np.insert(y_true_orig[:, 1], 0, history_y[-1])
    true_z = np.insert(y_true_orig[:, 2], 0, history_z[-1])
    
    pred_x = np.insert(y_pred_orig[:, 0], 0, history[-1])
    pred_y = np.insert(y_pred_orig[:, 1], 0, history_y[-1])
    pred_z = np.insert(y_pred_orig[:, 2], 0, history_z[-1])
    
    ax.plot(true_x, true_y, true_z, label='Ground Truth Future', color='blue', marker='o', markersize=4)
    ax.plot(pred_x, pred_y, pred_z, label=f'{model.name} Prediction', color='red', marker='x', linestyle='--', markersize=4)
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(f"3D Trajectory Overlay - Model: {model.name}")
    ax.legend()
    plt.show()

def plot_2d_trajectory_comparison(model, X_test, y_test, scaler_x, scaler_y, sample_idx=0):
    X_sample_scaled = X_test[sample_idx:sample_idx+1]
    y_true_scaled = y_test[sample_idx:sample_idx+1]
    y_pred_scaled = model.predict(X_sample_scaled, verbose=0)
    
    history = scaler_x['x'].inverse_transform(X_sample_scaled[:, :, 0].reshape(-1,1)).ravel()
    history_y = scaler_x['y'].inverse_transform(X_sample_scaled[:, :, 1].reshape(-1,1)).ravel()
    history_z = scaler_x['z'].inverse_transform(X_sample_scaled[:, :, 2].reshape(-1,1)).ravel()
    
    y_true_orig = inverse_transform_y(y_true_scaled, scaler_y)[0]
    y_pred_orig = inverse_transform_y(y_pred_scaled, scaler_y)[0]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    axes[0].plot(range(len(history)), history, color='gray', linestyle=':')
    axes[0].plot(range(len(history)-1, len(history)+len(y_true_orig)), np.insert(y_true_orig[:, 0], 0, history[-1]), label='Ground Truth', color='blue', marker='o')
    axes[0].plot(range(len(history)-1, len(history)+len(y_pred_orig)), np.insert(y_pred_orig[:, 0], 0, history[-1]), label='Predicted', color='red', marker='x', linestyle='--')
    axes[0].set_title('X Axis')
    axes[0].set_xlabel('Time Step')
    axes[0].set_ylabel('X (m)')
    axes[0].legend()
    
    axes[1].plot(range(len(history_y)), history_y, color='gray', linestyle=':')
    axes[1].plot(range(len(history_y)-1, len(history_y)+len(y_true_orig)), np.insert(y_true_orig[:, 1], 0, history_y[-1]), label='Ground Truth', color='blue', marker='o')
    axes[1].plot(range(len(history_y)-1, len(history_y)+len(y_pred_orig)), np.insert(y_pred_orig[:, 1], 0, history_y[-1]), label='Predicted', color='red', marker='x', linestyle='--')
    axes[1].set_title('Y Axis')
    axes[1].set_xlabel('Time Step')
    axes[1].set_ylabel('Y (m)')
    axes[1].legend()
    
    axes[2].plot(range(len(history_z)), history_z, color='gray', linestyle=':')
    axes[2].plot(range(len(history_z)-1, len(history_z)+len(y_true_orig)), np.insert(y_true_orig[:, 2], 0, history_z[-1]), label='Ground Truth', color='blue', marker='o')
    axes[2].plot(range(len(history_z)-1, len(history_z)+len(y_pred_orig)), np.insert(y_pred_orig[:, 2], 0, history_z[-1]), label='Predicted', color='red', marker='x', linestyle='--')
    axes[2].set_title('Z Axis')
    axes[2].set_xlabel('Time Step')
    axes[2].set_ylabel('Z (m)')
    axes[2].legend()
    
    plt.suptitle(f"2D Trajectory Component Overlay - Model: {model.name}")
    plt.tight_layout()
    plt.show()

def plot_full_trajectory_simulation(model, raw_data, trajectory_idx, scaler_x, scaler_y, T, H, sequence_length):
    trajectory = raw_data[trajectory_idx * sequence_length : (trajectory_idx + 1) * sequence_length]
    if trajectory.shape != (sequence_length, 3): return
    
    X_traj = []
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
        X_traj.append(input_sequence)
        
    X_traj = np.array(X_traj)
    
    num_samples = len(X_traj)
    X_scaled = np.zeros_like(X_traj)
    X_scaled[:, :, 0] = scaler_x['x'].transform(X_traj[:, :, 0].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 1] = scaler_x['y'].transform(X_traj[:, :, 1].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 2] = scaler_x['z'].transform(X_traj[:, :, 2].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 3] = scaler_x['vx'].transform(X_traj[:, :, 3].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 4] = scaler_x['vy'].transform(X_traj[:, :, 4].reshape(-1, 1)).reshape(num_samples, T)
    X_scaled[:, :, 5] = scaler_x['vz'].transform(X_traj[:, :, 5].reshape(-1, 1)).reshape(num_samples, T)
    
    y_pred_scaled = model.predict(X_scaled, verbose=0)
    y_pred_orig = inverse_transform_y(y_pred_scaled, scaler_y)
    
    pred_H_ahead = y_pred_orig[:, -1, :]
    time_steps_pred = np.arange(H-1, sequence_length)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    axes[0].plot(range(sequence_length), trajectory[:, 0], label='Ground Truth', color='blue')
    axes[0].plot(time_steps_pred, pred_H_ahead[:, 0], label=f'Predicted (H={H} ahead)', color='red', linestyle='--')
    axes[0].set_title('X Axis (Full Trajectory)')
    axes[0].set_xlabel('Time Step')
    axes[0].set_ylabel('X (m)')
    axes[0].legend()
    
    axes[1].plot(range(sequence_length), trajectory[:, 1], label='Ground Truth', color='blue')
    axes[1].plot(time_steps_pred, pred_H_ahead[:, 1], label=f'Predicted (H={H} ahead)', color='red', linestyle='--')
    axes[1].set_title('Y Axis (Full Trajectory)')
    axes[1].set_xlabel('Time Step')
    axes[1].set_ylabel('Y (m)')
    axes[1].legend()
    
    axes[2].plot(range(sequence_length), trajectory[:, 2], label='Ground Truth', color='blue')
    axes[2].plot(time_steps_pred, pred_H_ahead[:, 2], label=f'Predicted (H={H} ahead)', color='red', linestyle='--')
    axes[2].set_title('Z Axis (Full Trajectory)')
    axes[2].set_xlabel('Time Step')
    axes[2].set_ylabel('Z (m)')
    axes[2].legend()
    
    plt.suptitle(f"Full Trajectory Continuous Simulation - Model: {model.name}")
    plt.tight_layout()
    plt.show()

best_model_name = 'Seq2Seq'
if best_model_name in models_dict:
    sample_idx = np.random.randint(0, len(X_test_s))
    plot_3d_trajectory_comparison(models_dict[best_model_name], X_test_s, y_test_s, scaler_x, scaler_y, sample_idx=sample_idx)
    plot_2d_trajectory_comparison(models_dict[best_model_name], X_test_s, y_test_s, scaler_x, scaler_y, sample_idx=sample_idx)
    plot_3d_trajectory_comparison(models_dict['Direct_MultiOutput'], X_test_s, y_test_s, scaler_x, scaler_y, sample_idx=sample_idx)
    plot_2d_trajectory_comparison(models_dict['Direct_MultiOutput'], X_test_s, y_test_s, scaler_x, scaler_y, sample_idx=sample_idx)
    
    num_test_trajectories = len(raw_test) // SEQUENCE_LENGTH
    if num_test_trajectories > 0:
        traj_idx = np.random.randint(0, num_test_trajectories)
        plot_full_trajectory_simulation(models_dict[best_model_name], raw_test, traj_idx, scaler_x, scaler_y, T, H, SEQUENCE_LENGTH)
        plot_full_trajectory_simulation(models_dict['Direct_MultiOutput'], raw_test, traj_idx, scaler_x, scaler_y, T, H, SEQUENCE_LENGTH)
"""
add_code(code6)

with open('/home/duy/cocarry_ws/src/GRU-Model/Multi_Step_Prediction.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook generated successfully via json.")
