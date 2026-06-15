import xmlrpc.client
import time

def run_test():
    print("="*50)
    print("KỊCH BẢN KIỂM THỬ CƠ SỞ DỮ LIỆU PHÂN TÁN PUPDB")
    print("="*50)

    # Client chỉ giao tiếp với Proxy Router duy nhất ở port 8000
    proxy_url = "http://localhost:8000"
    print(f"[*] Đang kết nối tới Proxy tại {proxy_url}...")
    
    try:
        db = xmlrpc.client.ServerProxy(proxy_url)
    except Exception as e:
        print("[Lỗi] Không thể kết nối tới Proxy. Hãy chắc chắn proxy_router.py đang chạy!")
        return

    print("\n--- 1. KIỂM TRA GHI DỮ LIỆU (SHARDING & REPLICATION) ---")
    data_to_insert = {
        "sinhvien_01": "Nguyen Van A - KTPM",
        "sinhvien_02": "Tran Thi B - KHMT",
        "sinhvien_03": "Le Van C - HTTT",
        "sinhvien_04": "Pham Thi D - ATTT"
    }

    for key, value in data_to_insert.items():
        print(f"-> Ghi: {key} = {value}")
        db.set(key, value)
        time.sleep(0.5) # Dừng một chút để dễ quan sát log

    print("\n--- 2. KIỂM TRA ĐỌC DỮ LIỆU BÌNH THƯỜNG ---")
    for key in data_to_insert.keys():
        val = db.get(key)
        print(f"<- Đọc: {key} => Lấy được: {val}")

    print("\n" + "="*50)
    print("THỬ THÁCH CHỊU LỖI (FAULT TOLERANCE TEST)")
    print("="*50)
    print("Bây giờ, bạn hãy sang cửa sổ Terminal đang chạy Node 8001 hoặc 8002.")
    print("Nhấn Ctrl+C để tắt Node đó (Giả lập Master bị sập nguồn/mất mạng).")
    input(">>> Khi nào tắt xong Node Master, hãy nhấn ENTER tại đây để tiếp tục... <<<")

    print("\n--- 3. KIỂM TRA ĐỌC DỮ LIỆU KHI MASTER ĐÃ SẬP (FAILOVER) ---")
    print("[*] Hệ thống vẫn phải trả về dữ liệu bình thường nhờ đọc từ Slave Backup:")
    for key in data_to_insert.keys():
        val = db.get(key)
        print(f"<- Đọc: {key} => Lấy được: {val}")
        time.sleep(0.5)
    
    print("\n[THÀNH CÔNG] Hoàn tất kịch bản kiểm thử!")

if __name__ == "__main__":
    run_test()