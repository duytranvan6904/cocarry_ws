Dựa trên bài toán cùng khiêng vật (Co-carrying) sử dụng mô hình Deep-GRU của bạn trong tài liệu main.pdf và nền tảng kiến thức về điều khiển bám sát quỹ đạo từ bài báo tham khảo, dưới đây là sơ đồ điều khiển và hướng dẫn triển khai chi tiết để tích hợp MPC với mô hình Deep-GRU cho Cobot 7-DOF.

### 1\. Sơ đồ điều khiển tổng quát (System Architecture)

Lấy cảm hứng từ cấu trúc điều khiển bám chân người 1 và điều chỉnh cho phù hợp với bài toán Co-carrying của bạn 2, hệ thống sẽ bao gồm 4 khối chức năng chính hoạt động nối tiếp nhau trong thời gian thực:

* **Khối 1: Thu thập & Tiền xử lý dữ liệu (Sensing & Preprocessing):** Sử dụng camera RGB-D (như Intel RealSense D435i) kết hợp thuật toán theo dõi khung xương (MediaPipe) để trích xuất tọa độ 3D của tay người 3, 4\. Dữ liệu này được tính toán vận tốc và tạo thành vector trạng thái 6 chiều $ x, y, z, v\_x, v\_y, v\_z $ 5, 6\.  
* **Khối 2: Bộ dự đoán ý định (Deep-GRU Human Intent Predictor):** Lấy đầu vào là một chuỗi lịch sử (sliding window) của vector 6D trong 1 khoảng thời gian (ví dụ 1.25s) 7\. Mô hình Deep-GRU 3 lớp sẽ suy luận để xuất ra dự đoán về tọa độ 3D của tay người $\\hat{y}\_{t+T\_s}$ trong tương lai ngắn hạn (0.3s tới) 8, 9\.  
* **Khối 3: Bộ quy hoạch quỹ đạo (MPC Trajectory Planner):** Nhận dữ liệu là **chuỗi quỹ đạo 3D dự đoán** từ Khối 2 và **trạng thái hiện tại của robot** (góc khớp $\\theta$, vận tốc $\\dot{\\theta}$). Khối này giải một bài toán tối ưu hóa để tìm ra quỹ đạo chuyển động lý tưởng nhất cho 7 khớp của cobot, đáp ứng được hàm mục tiêu (chi phí) đã đặt ra 1, 10\.  
* **Khối 4: Bộ điều khiển cấp thấp (Robot Feedback Controller):** Nhận tín hiệu điều khiển tối ưu (tọa độ/vận tốc khớp) từ bộ MPC và ra lệnh cho các động cơ trên cobot (ví dụ bộ điều khiển YRC1000u của Yaskawa) thực thi.

### 2\. Chi tiết các thành phần trong Khối MPC (Cost Functions)

Nguyên lý của MPC là tối ưu hóa một hàm chi phí $J$ trên một đường chân trời dự báo (0.3s) 10, 11\. Hàm chi phí $J$ của bạn sẽ bao gồm 4 thành phần sau:

* **1\. Terminal Cost (Chi phí đích đến):** Đảm bảo end-effector của robot tiến đến đúng vị trí kẹp vật tại thời điểm cuối cùng của khoảng dự đoán (0.3s). Vì bạn đang làm bài toán Co-carrying (khiêng chung một vật cứng) 12, khoảng cách giữa tay người và tay robot là một hằng số $p\_{offset}$ (kích thước của vật). Điểm đích của robot sẽ là: $x\_{del} \= \\mu\_{w}(t+T\_o) \+ p\_{offset}$, trong đó $\\mu\_{w}(t+T\_o)$ là điểm cuối trong chuỗi 3D mà Deep-GRU dự đoán 13\.  
* **2\. Stage Cost 1 \- Chi phí bám quỹ đạo (Tracking Cost):** Giảm thiểu khoảng cách giữa quỹ đạo của end-effector và chuỗi quỹ đạo di chuyển của tay người *tại từng bước thời gian (time steps)* trong mốc 0.3s 14\. Điều này giúp robot di chuyển đồng bộ, mượt mà theo hình dáng quỹ đạo tay người (cong, đi thẳng, v.v.) 15\.  
* **3\. Stage Cost 2 \- Chi phí giới hạn động học (Kinematic Constraints):** Đây là nơi bạn phát huy lợi thế của MPC. Bạn đưa các giới hạn về vận tốc tối đa $\\dot{\\theta}*{max}$ và gia tốc tối đa $\\ddot{\\theta}*{max}$ của 7 trục cobot vào hàm phạt 16, 17\. Nếu quỹ đạo tính toán đòi hỏi robot di chuyển quá nhanh (vượt quá ngưỡng cho phép), hàm chi phí này sẽ tăng vọt, buộc MPC phải tìm một quỹ đạo êm ái hơn, tránh tình trạng robot bị giật (kích hoạt torque limiter của cobot) 18\.  
* **4\. Stage Cost 3 \- Chi phí an toàn (Safety Cost):** Bài báo tham khảo sử dụng Trường thế nhân tạo dựa trên khoảng cách Mahalanobis vì mô hình GMR của họ xuất ra phương sai (độ bất định) 19\. Vì mô hình Deep-GRU của bạn là mô hình tất định (chỉ xuất ra 1 tọa độ chính xác) 8, 20, bạn có thể thay thế bằng **khoảng cách Euclid**. Nếu khoảng cách giữa các khớp của robot và tọa độ tay/cơ thể người nhỏ hơn một ngưỡng an toàn, chi phí này sẽ tăng mạnh để robot chủ động tận dụng bậc tự do thứ 7 (redundancy) lách qua hoặc giữ khoảng cách.

### 3\. Cách triển khai chi tiết vào hệ thống thực tế

**Bước 1: Chạy song song mô hình Deep-GRU và thu thập trạng thái**Bạn cần thiết lập một vòng lặp thu thập dữ liệu ở tốc độ cao. Dựa trên số liệu của bạn, Deep-GRU có thời gian suy luận chỉ khoảng 4ms (đáp ứng thông lượng \>250Hz) 21\. Khối này sẽ liên tục nhận dữ liệu từ MediaPipe và xuất ra chuỗi dự đoán (ví dụ 5 điểm tọa độ 3D trong 0.3s tương lai) và gửi sang bộ MPC.  
**Bước 2: Cập nhật hàm mục tiêu và giải bài toán MPC (Receding Horizon)**Tại mỗi chu kỳ điều khiển (ví dụ $t$), bộ MPC sẽ nhận chuỗi 5 điểm dự đoán này. Sử dụng phép tính biến phân (Calculus of Variations) hoặc một bộ giải tối ưu phi tuyến (như CasADi hoặc IPOPT trong Python/C++), thuật toán sẽ tìm kiếm chuỗi tín hiệu điều khiển góc khớp tối ưu $u(t), u(t+1), ..., u(t+T\_o)$ thỏa mãn các hàm chi phí ở phần 2 22, 23\.  
**Bước 3: Nguyên lý "Chân trời lùi" (Receding Horizon Execution)**Mặc dù bộ giải MPC tính toán ra một chuỗi lệnh điều khiển cho toàn bộ 0.3s tới, bạn **chỉ lấy lệnh điều khiển đầu tiên $u(t)$** để gửi xuống robot Yaskawa 1, 23\. Lý do là:

* Tay người có thể bất ngờ thay đổi hướng (Target Change) 24\.  
* Ở chu kỳ tiếp theo ($t+1$), mô hình Deep-GRU sẽ lại xuất ra một chuỗi dự đoán mới được cập nhật. Bạn tiếp tục giải MPC và lại chỉ lấy bước đầu tiên. Cơ chế này giúp robot liên tục "nhìn về tương lai" nhưng vẫn phản ứng nhanh chóng với các sai số trong thời gian hiện tại.

**Bước 4: Xuất tín hiệu cho robot** Sử dụng các thư viện giao tiếp real-time (như motoROS hoặc truyền nhận UDP trực tiếp) để gửi tín hiệu vận tốc khớp $\\dot{\\theta}$ hoặc góc khớp $\\theta$ mục tiêu xuống bộ điều khiển. Nhờ giới hạn của Stage Cost 2, bạn có thể tự tin gửi lệnh chạy thẳng mà không sợ robot vi phạm các chuẩn an toàn vật lý của chính nó.  
