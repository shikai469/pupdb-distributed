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