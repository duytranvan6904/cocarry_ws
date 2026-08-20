Baseline so sánh:

1. Baseline 1 (Ground Truth): Chỉ sử dụng feedback vị trí trực tiếp từ camera.  
2. Baseline 2 (Prediction Only): Sử dụng feedback vị trí \+ Mô hình học sâu dự đoán quỹ đạo (GRU) để bù trễ (bỏ qua kiểm soát công thái học).  
3. Proposed System (Adaptive Shared Control): Sử dụng toàn bộ framework đề xuất (Feedback vị trí \+ GRU Predictor \+ Đánh giá công thái học s\_e \+ Độ tin cậy dự đoán s\_r).

# KỊCH BẢN 1: BÀI TEST KIỂM TRA ĐỘ TRỄ VÀ TÍNH ĐỒNG BỘ CỦA ROBOT

**Mục đích trong ứng dụng thực tế:** Phục vụ các tác vụ cùng khiêng đồ vật thông thường trong công nghiệp hoặc sinh hoạt (như khiêng bàn ghế, dời vật nặng). Trong các tác vụ này, nếu robot phản hồi chậm sẽ tạo ra lực giằng co lên tay người dùng hoặc làm rơi rớt đồ vật.  
**Mục tiêu:** Chứng minh việc áp dụng mô hình mạng nơ-ron hồi quy sâu (Deep-GRU) để dự đoán quỹ đạo tương lai giúp giải quyết triệt để rào cản độ trễ vật lý của hệ thống camera thuần (Baseline 1).  
**Cách di chuyển**: Người tham gia cùng nâng một vật thể với robot (End-Effector) từ một vị trí xuất phát và di chuyển mượt mà tới một điểm đích đã được đánh dấu sẵn trong không gian.  
**Kết quả kỳ vọng:**

- Baseline 1: Robot phản hồi chậm, có độ trễ lớn (lagging) đi sau tay người.  
- Baseline 2 và Proposed System: Cho độ trễ cực thấp. Vị trí quỹ đạo tay người và EE của robot gần như trùng khớp lên nhau (chỉ cách nhau một khoảng tịnh tiến bằng đúng kích thước offset của vật thể).

**Thông số theo dõi**: Vận tốc di chuyển của bàn tay người (v\_hand) và vận tốc của EE (v\_ee) theo thời gian.  
**Cách đo đạc**: Vẽ và phân tích đồ thị vận tốc đồng bộ thời gian. Trích xuất khoảng thời gian trễ được tính từ mốc thời gian tay người bắt đầu nhúc nhích cho đến khi robot bắt đầu di chuyển tương ứng.

# KỊCH BẢN 2: XỬ LÝ CÁC TÌNH HUỐNG GIẬT CỤC NGOÀI Ý MUỐN

**Mục đích trong ứng dụng thực tế:** Đảm bảo an toàn lao động. Trong quá trình di chuyển, người dùng có thể gặp tai nạn (trượt chân, trượt tay, hắt hơi...) làm quỹ đạo tay bị văng đi đột ngột. Nếu robot cường lực đang giữ vật nặng mà cũng lao theo gia tốc đó thì sẽ gây nguy hiểm nghiêm trọng.  
**Mục tiêu:** Làm nổi bật hiệu năng của Module A (Prediction Reliability \- s\_r). Khẳng định tính an toàn của hệ thống khi mô hình đưa ra dự đoán sai do nhiễu ngoại cảnh đột ngột.  
**Cách di chuyển**: Người tham gia đang di chuyển tay êm ái cùng robot theo một đường thẳng, sau đó cố tình giật tay rất mạnh sang một hướng khác (mô phỏng trượt tay/vấp ngã) rồi dừng lại.  
**Kết quả kỳ vọng:**

- Baseline 1 & 2: Sinh ra độ giật (Jerk) rất lớn ở tay máy do nhận trực tiếp vị trí tay từ camera hoặc do mô hình cố gắng bù trễ theo gia tốc đó.  
- Proposed System: Khi tay giật đột ngột, khoảng cách giữa tọa độ dự đoán (Prediction) và vị trí thực tế (Ground Truth) lớn đột biến. Điểm tin cậy s\_r lập tức tụt xuống. Kéo theo trọng số w giảm mạnh, giúp hãm phanh robot lại một cách êm ái thay vì lao văng theo người dùng. Robot duy trì được tính ổn định.

**Thông số theo dõi**: Độ giật (Jerk) của tay người và robot; Giá trị độ tin cậy s\_r; Trọng số làm mượt quỹ đạo w  
**Cách đo đạc**: Đặt 3 đồ thị lên cùng một trục thời gian: (1) Quỹ đạo Jerk của tay người & Robot, (2) Đồ thị s\_r, (3) Đồ thị w. Đối chiếu thời điểm xảy ra sự cố (Jerk tay người đạt đỉnh) với khoảnh khắc s\_r rớt chạm đáy để chứng minh sự can thiệp tức thời của hệ thống.

# KỊCH BẢN 3: BÀI TEST VƯỢT QUÁ TẦM VỚI 

**Mục đích trong ứng dụng thực tế**: Trong công nghiệp, công nhân thường phải cùng robot khiêng các bộ phận cồng kềnh (như tấm kính) và lách/xoay chúng vào các vị trí hẹp. Thay vì xoay cả thân người (bước chân) để đổi hướng, người lao động thường có thói quen đứng yên tại chỗ và chỉ dùng cánh tay để vặn xoắn. Thói quen này tích tụ lâu ngày là nguyên nhân hàng đầu gây chấn thương cơ xương khớp ở công nhân.

**Mục tiêu**: Chứng minh hệ thống đánh giá công thái học (Ergonomics Tracking) có khả năng phát hiện tư thế vặn xoắn nguy hiểm, đồng thời sử dụng chính sự chậm lại của robot như một cơ chế phản hồi lực (Haptic Feedback) vô hình, nhắc nhở và ép buộc công nhân phải chỉnh lại tư thế (bước chân) thay vì vặn tay.

**Cách di chuyển:** người tham gia và End-Effector của robot cùng giữ một vật. Đặt một mục tiêu ở khoảng cách xa (nằm ngoài giới hạn sải tay bình thường). Yêu cầu người dùng với tới mục tiêu đó mà không được bước chân lên (bắt buộc phải nhô vai, rướn ngực, sai tư thế).  
**Kết quả kỳ vọng:**

- Baseline 1 & 2: Robot lao thẳng tới đích cùng người dùng, vô tình cho phép tư thế sai diễn ra. Hậu quả: Người lao động hoàn thành thao tác dễ dàng nhưng hệ thống vô tình "tiếp tay" cho thói quen làm việc sai tư thế, rủi ro chấn thương tay là rất cao. Điểm RULA trung bình trong quá trình làm việc cao.  
- Proposed System: Khi người dùng bắt đầu rướn vai, điểm RULA tăng lên làm điểm thoải mái s\_e giảm mạnh —\> trọng số w tụt xuống gần 0\. Tọa độ mục tiêu nội suy p\_raw tự động trượt về vị trí phản hồi hiện tại p\_fb của robot. Kết quả là robot nặng nề hơn, dừng lại và tạo ra một "bức tường ảo" (Virtual Damping). Sự khựng lại này ép người lao động không thể vặn tay thêm được nữa, bắt buộc họ phải nhấc chân, xoay cả cơ thể hướng theo vật thể để đưa các khớp tay về lại tư thế thẳng tự nhiên thì robot mới tiếp tục bám sát mượt mà giúp điểm RULA trung bình thấp hơn. 

**Thông số theo dõi:** Tọa độ 3D của End-Effector (p\_fb) và tay người (p\_hand); Điểm công thái học s\_e; Điểm RULA (để minh chứng tư thế xấu); Trọng số w; Biến thiên các góc động học tay dễ chấn thương sinh ra từ hệ thống MediaPipe: Góc khuỷu tay ($\\alpha\_c$) và Góc bẻ cổ tay ($\\gamma\_s$).  
**Cách đo đạc**: Cách đo đạc:

- Vẽ đồ thị đồng bộ thời gian của các góc $\\alpha\_c$ và $\\gamma\_s$.  
- Đo đạc Tích phân của sai số góc (Diện tích dưới biểu đồ \- Area Under Curve) đối với các khoảng thời gian góc vượt ngưỡng an toàn (ví dụ: góc cổ tay \> 15 độ).  
- Minh chứng: Ở Baseline 1 & 2, diện tích phần quá ngưỡng sẽ rất lớn (chứng tỏ tay bị bẻ cong trong thời gian dài). Còn ở Proposed System, đồ thị góc sẽ bị cắt phẳng (Cut-off) ở ngưỡng an toàn, diện tích quá ngưỡng cực kỳ nhỏ vì robot đã ngắt nhịp chuyển động trước khi tay người kịp vẹo sâu hơn.  
- Vẽ đồ thị thang điểm RULA theo thời gian, tính điểm trung bình trong các trial của người tham gia.


