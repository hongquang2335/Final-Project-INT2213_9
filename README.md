# Project 2: Intra-Domain Routing Algorithms

## Thành viên nhóm

1: Đầu Hồng Quang - 23020135
2: Đỗ Đình Nam - 23020120

## Giới thiệu đề tài

Internet không phải là một mạng duy nhất mà bao gồm nhiều mạng độc lập, gọi là "hệ thống tự trị" (Autonomous Systems - AS). Trong đó, mỗi AS thuộc sở hữu và điều hành bởi một tổ chức riêng như một ISP, một công ty, hay một trường đại học; và các AS này phải phối hợp với nhau để gói tin có thể được chuyển từ máy gửi đến máy nhận, kể cả khi hai máy nằm trong 2 AS khác nhau. Khi ấy, việc định tuyến AS trở nên phức tạp, không chỉ phụ thuộc vào việc lựa chọn đường đi ngắn nhất mà còn phụ thuộc vào các yếu tố khác như chính sách kinh doanh, chính sách kĩ thuật, ...

Đề tài này tập trung vào các thuật toán định tuyến nội miền (intra-domain routing), tức chỉ tập trung nghiên cứu về định tuyến bên trong một AS duy nhất, với mục tiêu là tìm đường đi ngắn nhất / rẻ nhất từ điểm A tới điểm B trong cùng một mạng. Điểm thuận lợi ở đây là vì tất cả các router đã nằm trong 1 AS - thuộc quản lí của một đơn vị, nên có thể phối hợp chặt chẽ và dễ dàng hơn.

Do tính chất mạng thường xuyên có sự thay đổi: mất kết nối giữa các router, hỏng liên kết, thay đổi tải, ... cũng như việc các router không thể có thông tin của cả mạng ngay từ đầu mà chỉ khởi đầu với các thông tin cục bộ (biết về các liên kết trực tiếp với nó) nên cần thuật toán phân tán để xây dựng bảng định tuyến toàn diện cho cả mạng, cũng như giúp router tự động cập nhật đường đi tối ưu.

Hầu hết các thuật toán định tuyến nội miền đều thuộc một trong hai loại, 
distance - vector(DV) hoặc link - state(LS). Trong đề tài này, chúng em sẽ nghiên cứu và triển khai đơn giản về thuật toán DV.

## Distance vector Routing

### Khái niệm

Là thuật toán định tuyến phân tán, trong đó:
- Mỗi router tự tính cost từ nó đến mọi đích trong mạng.
- Mỗi router trao đổi định tuyến với các router lân cận(có liên kết trực tiếp với nó) để cập nhật bảng định tuyến của mình.

### Tính chất

1. Mỗi router sẽ duy trì một distance vector, tức một bảng lưu thông tin về đường đi tới các router khác. Khởi tạo ban đầu, router biết khoảng cách đến chính nó là 0, còn lại khởi tạo oo.
2. Mỗi khi router nhận được distance vector từ các router lân cận, nó so sánh chi phí mới đến mỗi đích với chính distance router của nó, nếu chi phí rẻ hơn thì cập nhật bảng định tuyến và đistance vector (tuơng tự thuật toán Ford - Bellman).
3. Nếu distance vector của nó thay đổi, một bản ghi sẽ được gửi trực tiếp tới các router lân cận để cập nhật.
4. Ngay cả khi không có thay đổi, một bản ghi vẫn sẽ được gửi theo định kì để đảm bảo thông tin không bị lỗi/mất.
5. Mỗi router chỉ gửi distance vector của chính nó, không gửi bản của router khác gửi cho nó, tránh vòng lặp và tránh gửi thông tin không cần thiết.

## Lập trình

### Download + Setup mô phỏng mạng

### Yêu cầu bài toán

Xem chi tiết [tại đây](https://github.com/Harvard-CS145/routing?tab=readme-ov-file#implementation-instructions).

### Chạy và Kiểm thử

Dự án đã có sẵn bộ test kiểm thử tương ứng.

1. Để chạy dự án với giao diện đồ hoạ bằng lệnh:
`python3 visualize_network.py [NetworkSimulationFile.json] DV`

Ví dụ với small_net: 
`python3 visualize_network.py [01_small_net.json] DV`

2. Để chạy dự án không có giao diện đồ hoạ bằng lệnh:
`python3 network.py [NetworkSimulationFile.json] DV`

Ví dụ với small_net: 
`python3 network.py [01_small_net.json] DV`

Các tuyến đường đến và đi với mỗi client sau khi kết thúc quá trình chạy mô phỏng sẽ được in ra, cùng với việc chúng có khớp kết quả test đưa ra hay không. Nếu khớp, việc triển khai thành công, ngược lại nếu không, tiếp tục fix bug.
