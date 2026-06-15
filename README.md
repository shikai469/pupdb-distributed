# Nâng cấp PupDB thành Cơ sở dữ liệu Phân tán (Distributed Database)

## 1. Giới thiệu dự án
Dự án này là bài tập lớn môn **Ứng dụng Phân tán**, nhằm mục đích nâng cấp mã nguồn của CSDL cục bộ [PupDB](https://github.com/tuxmonk/pupdb) thành một hệ thống phân tán thực thụ. 

Dự án áp dụng các kiến thức cốt lõi:
- **Định danh & Không gian tên:** Áp dụng thuật toán băm (Modulo Hashing) để phân mảnh dữ liệu (Sharding).
- **Truyền thông:** Sử dụng RPC (Remote Procedure Call) để các Node giao tiếp qua mạng.
- **Tính chịu lỗi (Fault Tolerance):** Che giấu lỗi bằng sự dư thừa thông tin qua mô hình Master - Slave Replication. Cơ chế Failover tự động chuyển hướng đọc dữ liệu khi Node chính gặp sự cố.

## 2. Kiến trúc hệ thống
Hệ thống sử dụng mô hình Client - Proxy - Storage Nodes:
- **Proxy Router (Port 8000):** Cổng giao tiếp duy nhất với Client. Làm nhiệm vụ định tuyến, băm khóa dữ liệu và quản lý lỗi.
- **Cụm Shard 0:** Gồm Master Node (Port 8001) và Slave Node (Port 9001).
- **Cụm Shard 1:** Gồm Master Node (Port 8002) và Slave Node (Port 9002).

Khi ghi dữ liệu, Proxy ghi vào Master và tự động nhân bản (Replicate) sang Slave. Khi đọc dữ liệu, nếu Master sập, Proxy tự động đọc từ Slave (Failover) giúp hệ thống luôn trong trạng thái Sẵn sàng (High Availability).

## 3. Hướng dẫn cài đặt và chạy thử
**Yêu cầu:** Môi trường Python 3.x và thư viện `filelock`.

```bash
pip install filelock
```

## 4. Khởi chạy hệ thống
Để mô phỏng mạng phân tán ở máy cục bộ (localhost), bạn cần mở 6 cửa sổ Terminal (hoặc Command Prompt) riêng biệt tại thư mục gốc của dự án và chạy các lệnh dưới đây theo đúng thứ tự:

**Bước 1: Khởi động các Node lưu trữ (Storage Nodes)**

Terminal 1: Khởi động Shard 0 Master

```bash
python node_server.py 8001
```
Terminal 2: Khởi động Shard 0 Slave

```bash
python node_server.py 9001
```
Terminal 3: Khởi động Shard 1 Master

```bash
python node_server.py 8002
```
Terminal 4: Khởi động Shard 1 Slave

```bash
python node_server.py 9002
```
**Bước 2: Khởi động Bộ định tuyến trung tâm (Proxy Router)**

Terminal 5: Khởi động Proxy

```bash
python proxy_router.py
```
**Bước 3: Chạy kịch bản kiểm thử (Test Client)**

Terminal 6: Chạy Client để kiểm tra tính năng phân mảnh và chịu lỗi

```bash
python client.py
```
💡 Mẹo kiểm thử Tính chịu lỗi: Khi chạy script ở Bước 3, hệ thống sẽ tạm dừng và yêu cầu bạn tắt thử 1 Node Master (bằng cách ấn Ctrl + C ở Terminal 1 hoặc 3). Sau khi tắt xong, ấn Enter ở Terminal 6 để thấy hệ thống tự động đọc dữ liệu từ Node Slave như thế nào!
