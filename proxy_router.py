import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

# Cấu trúc Master - Slave (Áp dụng Che giấu lỗi bằng sự dư thừa - Chương 8)
CLUSTER = {
    "shard_0": {"master": "http://localhost:8001", "slave": "http://localhost:9001"},
    "shard_1": {"master": "http://localhost:8002", "slave": "http://localhost:9002"}
}

def get_shard(key):
    # Thuật toán phân mảnh (Sharding)
    shard_keys = list(CLUSTER.keys())
    shard_index = hash(key) % len(shard_keys)
    return shard_keys[shard_index]

def set_key(key, value):
    shard_id = get_shard(key)
    master_url = CLUSTER[shard_id]["master"]
    slave_url = CLUSTER[shard_id]["slave"]
    
    # 1. Luôn ghi vào Master đầu tiên
    try:
        master_client = xmlrpc.client.ServerProxy(master_url)
        master_client.set(key, value)
        print(f"[Proxy] Đã ghi '{key}' vào Master ({master_url})")
    except Exception:
        print(f"[Lỗi] Master {master_url} sập! Không thể ghi dữ liệu.")
        return False

    # 2. Đồng bộ hóa dữ liệu (Replication) sang Slave ngay lập tức
    try:
        slave_client = xmlrpc.client.ServerProxy(slave_url)
        slave_client.set(key, value)
        print(f"[Proxy] Đã nhân bản '{key}' sang Slave ({slave_url})")
    except Exception:
        print(f"[Cảnh báo] Slave {slave_url} sập! Dữ liệu chưa được nhân bản.")
    
    return True

def get_key(key):
    shard_id = get_shard(key)
    master_url = CLUSTER[shard_id]["master"]
    slave_url = CLUSTER[shard_id]["slave"]
    
    # CƠ CHẾ CHỊU LỖI (FAILOVER READ)
    try:
        # Thử đọc từ Master trước
        master_client = xmlrpc.client.ServerProxy(master_url)
        return master_client.get(key)
    except Exception:
        # Che giấu lỗi: Tự động chuyển sang đọc ở Slave mà Client không hề hay biết
        print(f"[*] Phát hiện Master {master_url} lỗi. Đang Failover sang Slave {slave_url}...")
        try:
            slave_client = xmlrpc.client.ServerProxy(slave_url)
            return slave_client.get(key)
        except Exception:
            print(f"[Lỗi] Toàn bộ cụm {shard_id} đã sập!")
            return None

# Khởi chạy Proxy Server
proxy_server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
proxy_server.register_function(set_key, "set")
proxy_server.register_function(get_key, "get")

print("[*] Central Proxy Router (Sharding & Fault Tolerance) đang chạy tại http://localhost:8000")
proxy_server.serve_forever()