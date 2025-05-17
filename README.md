# 🚀 Project 2: Intra-Domain Routing Algorithms

## 👥 Thành viên nhóm

1. **Đầu Hồng Quang** - 23020135
2. **Đỗ Đình Nam** - 23020120

---

## 📘 Giới thiệu đề tài

Mạng Internet không phải là một mạng duy nhất, mà là tập hợp của nhiều mạng độc lập gọi là **Autonomous Systems (AS)**. Mỗi AS thường do một tổ chức như nhà cung cấp dịch vụ Internet (ISP), doanh nghiệp, hoặc trường đại học điều hành. Để các gói tin có thể di chuyển giữa các AS, cần có sự phối hợp định tuyến giữa chúng.

Tuy nhiên, đề tài này **tập trung vào định tuyến nội miền (intra-domain routing)** – tức việc tìm đường đi tối ưu trong phạm vi một AS. Vì tất cả các router trong cùng một AS được quản lý bởi một tổ chức, nên việc phối hợp và chia sẻ thông tin định tuyến có thể thực hiện hiệu quả hơn.

Trong môi trường mạng luôn thay đổi (liên kết hỏng, router mất kết nối, tải thay đổi, v.v), các router cần thuật toán định tuyến phân tán để xây dựng và cập nhật bảng định tuyến dựa trên thông tin cục bộ.

---

## 🧠 Thuật toán sử dụng: Link-State Routing (LS)

Thuật toán định tuyến **Link-State (LS)** là một trong hai nhóm chính của định tuyến nội miền (bên cạnh Distance-Vector). Trong mô hình LS:

* Mỗi router chỉ biết thông tin về các liên kết trực tiếp của nó.
* Router phát tán thông tin trạng thái liên kết (Link-State Advertisements - LSA) đến tất cả các router khác.
* Mỗi router xây dựng cơ sở dữ liệu link-state (LSDB) chứa bản đồ toàn mạng.
* Thuật toán **Dijkstra** được sử dụng để tính đường đi ngắn nhất từ router đến tất cả các đích khác.
* Thông tin được cập nhật định kỳ hoặc khi có thay đổi.

### 🔍 Các thành phần chính

1. **LSDB (Link-State Database)**
   Lưu trữ thông tin trạng thái của chính router và các router khác trong mạng.

2. **Lan truyền LSA**
   Router gửi và chuyển tiếp LSA đến các hàng xóm khi có thay đổi, hoặc theo định kỳ.

3. **Tính toán đường đi**
   Dựa trên LSDB, thuật toán Dijkstra được sử dụng để xây dựng bảng định tuyến.

4. **Phiên bản và cập nhật**
   Mỗi LSA có sequence number để đảm bảo router luôn giữ phiên bản mới nhất.

---

## 💻 Hướng dẫn cài đặt

*(Để trống theo yêu cầu)*

---

## 🧪 Hướng dẫn chạy mô phỏng & kiểm thử

### 1. Mô phỏng với giao diện đồ hoạ (GUI)

```bash
python3 visualize_network.py [NetworkSimulationFile.json] LS
```

**Ví dụ:**

```bash
python3 visualize_network.py 01_small_net.json LS
```

### 2. Mô phỏng không có giao diện đồ hoạ

```bash
python3 network.py [NetworkSimulationFile.json] LS
```

**Ví dụ:**

```bash
python3 network.py 01_small_net.json LS
```

---

Sau khi chạy, chương trình sẽ hiển thị các tuyến đường đến/đi của mỗi router. Kết quả sẽ được đối chiếu với tập test mẫu:

* ✅ Nếu khớp với kết quả mẫu → triển khai đúng.
* ❌ Nếu sai → cần rà soát lại thuật toán hoặc dữ liệu.

---

## 🔗 Tài liệu tham khảo

* [Harvard CS145 - Routing Project](https://github.com/Harvard-CS145/routing?tab=readme-ov-file#implementation-instructions)

