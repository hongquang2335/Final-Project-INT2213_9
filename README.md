# Project 2: Intra-Domain Routing Algorithms

## Thành viên nhóm

1. Đầu Hồng Quang - 23020135
2. Đỗ Đình Nam - 23020120

## Giới thiệu đề tài

Internet không phải là một mạng duy nhất mà bao gồm nhiều mạng độc lập, gọi là "hệ thống tự trị" (Autonomous Systems - AS). Trong đó, mỗi AS thuộc sở hữu và điều hành bởi một tổ chức riêng như một ISP, một công ty, hay một trường đại học; và các AS này phải phối hợp với nhau để gói tin có thể được chuyển từ máy gửi đến máy nhận, kể cả khi hai máy nằm trong 2 AS khác nhau. Khi ấy, việc định tuyến AS trở nên phức tạp, không chỉ phụ thuộc vào việc lựa chọn đường đi ngắn nhất mà còn phụ thuộc vào các yếu tố khác như chính sách kinh doanh, chính sách kĩ thuật, ...

Đề tài này tập trung vào các thuật toán định tuyến nội miền (intra-domain routing), tức chỉ tập trung nghiên cứu về định tuyến bên trong một AS duy nhất, với mục tiêu là tìm đường đi ngắn nhất / rẻ nhất từ điểm A tới điểm B trong cùng một mạng. Điểm thuận lợi ở đây là vì tất cả các router đã nằm trong 1 AS - thuộc quản lí của một đơn vị, nên có thể phối hợp chặt chẽ và dễ dàng hơn.

Do tính chất mạng thường xuyên có sự thay đổi: mất kết nối giữa các router, hỏng liên kết, thay đổi tải, ... cũng như việc các router không thể có thông tin của cả mạng ngay từ đầu mà chỉ khởi đầu với các thông tin cục bộ (biết về các liên kết trực tiếp với nó) nên cần thuật toán phân tán để xây dựng bảng định tuyến toàn diện cho cả mạng, cũng như giúp router tự động cập nhật đường đi tối ưu.

Hầu hết các thuật toán định tuyến nội miền đều thuộc một trong hai loại, 
distance - vector(DV) hoặc link - state(LS). Trong đề tài này, chúng em sẽ nghiên cứu và triển khai đơn giản về thuật toán LS.

## Link State Routing

### Khái niệm

Là một thuật toán định tuyến phân tán, trong đó:
- Mỗi router duy trì thông tin trạng thái liên kết (link-state) của chính nó và các router khác.
- Mỗi router tự tính toán đường đi tốt nhất đến mọi đích dựa trên toàn bộ bản đồ mạng thu được.
- Router trao đổi thông tin trạng thái liên kết với các hàng xóm để cập nhật cơ sở dữ liệu trạng thái mạng.

### Tính chất

1. Link-State Database (LSDB):
- Mỗi router lưu trạng thái liên kết của chính nó: danh sách các liên kết tới hàng xóm và trọng số.
- Đồng thời lưu thông tin link-state của các router khác thông qua quá trình lan truyền.
2. Lan truyền thông tin:
- Khi có thay đổi trong trạng thái liên kết, router sẽ phát đi gói tin link-state (LSA – Link-State Advertisement) cho tất cả các hàng xóm.
- Mỗi router lan truyền tiếp LSA mà nó nhận được (ngoại trừ nơi gửi), giúp mọi router có cùng một LSDB.
3. Tính toán định tuyến:
- Khi LSDB được cập nhật, router sẽ sử dụng thuật toán Dijkstra để tính toán đường đi ngắn nhất đến mọi đích và cập nhật bảng định tuyến.
4. Gửi định kỳ:
- Ngay cả khi không có thay đổi, router vẫn phát link-state định kỳ để đảm bảo dữ liệu không bị lỗi hoặc mất đồng bộ.
5. Quản lý phiên bản (Sequence Number):
- Mỗi gói link-state kèm theo một sequence number để xác định phiên bản mới nhất.
- Nếu nhận được gói có sequence number cũ hơn, router sẽ bỏ qua, tránh cập nhật nhầm thông tin lỗi thời.

## Lập trình

### Download + Setup mô phỏng mạng

### Yêu cầu bài toán

Xem chi tiết [tại đây](https://github.com/Harvard-CS145/routing?tab=readme-ov-file#implementation-instructions).

### Chạy và Kiểm thử

Dự án đã có sẵn bộ test kiểm thử tương ứng.

1. Để chạy dự án với giao diện đồ hoạ bằng lệnh:
`python3 visualize_network.py [NetworkSimulationFile.json] LS`

Ví dụ với small_net: 
`python3 visualize_network.py 01_small_net.json LS`

2. Để chạy dự án không có giao diện đồ hoạ bằng lệnh:
`python3 network.py [NetworkSimulationFile.json] LS`

Ví dụ với small_net: 
`python3 network.py 01_small_net.json LS`

Các tuyến đường đến và đi với mỗi client sau khi kết thúc quá trình chạy mô phỏng sẽ được in ra, cùng với việc chúng có khớp kết quả test đưa ra hay không. Nếu khớp, việc triển khai thành công, ngược lại nếu không, tiếp tục fix bug.
