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

Dưới đây là hướng dẫn chi tiết cho trường hợp sử dụng Windows làm máy chủ (host) và Ubuntu trên máy ảo (guest), kèm SSH và X11 forwarding để chạy giao diện Tinker:

1. **Chuẩn bị máy ảo (VM)**

   * Cài đặt **VirtualBox** ([https://www.virtualbox.org/](https://www.virtualbox.org/)) hoặc **VMware Workstation Player**.
   * Tạo máy ảo mới, cài đặt **Ubuntu 20.04** (hoặc version tương đương).
   * Cấp đủ tài nguyên (RAM ≥ 4GB, CPU ≥ 2 cores) và mở cổng mạng ở chế độ **Bridged Adapter** hoặc **Host-only**.

2. **Cài đặt file yêu cầu của môn học**

   * Trên máy host Windows, mở PowerShell/Git Bash và clone cả hai repo:

     ```bash
     git clone https://github.com/Harvard-CS145/routing.git
     git clone -b spring2025 https://github.com/minlanyu/cs145-site.git
     ```
   * Chép nội dung thư mục `routing/` vào thư mục home của máy ảo (ví dụ `/home/ubuntu/routing`) qua SMB hoặc SCP:

     ```bash
     scp -r routing/ ubuntu@<VM_IP>:/home/ubuntu/
     ```

3. **Cài đặt và cấu hình SSH trên Ubuntu (guest)**

   * Trên máy ảo Ubuntu, chạy:

     ```bash
     sudo apt update
     sudo apt install -y openssh-server
     sudo systemctl enable ssh
     sudo systemctl start ssh
     sudo ufw allow OpenSSH
     ```
   * Xác định địa chỉ IP của VM:

     ```bash
     ip addr show
     ```

4. **Thiết lập SSH trong VSCode (host Windows)**

   * Cài đặt extension **Remote - SSH** trong VSCode.
   * Tạo (hoặc chỉnh) file cấu hình SSH `~/.ssh/config` trên Windows:

     ```text
     Host cs145-vm
         HostName <VM_IP>
         User ubuntu
         IdentityFile ~/.ssh/id_rsa
         ForwardX11 yes
         ForwardX11Trusted yes
     ```
   * Nếu chưa có khóa, tạo khóa RSA:

     ```bash
     ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
     ssh-copy-id ubuntu@<VM_IP>
     ```
   * Trong VSCode, chọn **Remote-SSH: Connect to Host... → cs145-vm**.

5. **Cài đặt X Server trên Windows (X11 forwarding)**

   * Tải và cài **Xming** hoặc **VcXsrv (Xlaunch)**:

     * Xming: [https://sourceforge.net/projects/xming/](https://sourceforge.net/projects/xming/)
     * VcXsrv: [https://sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/)
   * Khởi chạy Xlaunch với cấu hình:

     * Multiple windows
     * Display number: 0
     * Clipboard: Enable
     * Native OpenGL: Disable
   * Đảm bảo Windows Firewall cho phép Xming/VcXsrv.

6. **Kiểm thử X11 Forwarding và Tinker GUI**

   * Trong VSCode terminal (đang SSH vào VM), chạy:

     ```bash
     xeyes    # kiểm tra cửa sổ X11
     ```
   * Chạy mô phỏng Tinker:

     ```bash
     cd ~/routing
     python3 visualize_network.py 01_small_net.json LS
     ```
   * Giao diện Tinker sẽ hiện lên trên Windows qua Xming/VcXsrv.

7. **Các lệnh hữu ích**

   * Cập nhật gói Python và dependencies:

     ```bash
     sudo apt install -y python3-pip
     pip3 install -r requirements.txt
     ```
   * Kiểm tra trạng thái SSH:

     ```bash
     sudo systemctl status ssh
     ```
   * Thoát VSCode SSH:
     Chọn **Remote-SSH: Close Remote Connection**.

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
