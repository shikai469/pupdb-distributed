import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

# Giả sử chúng ta sẽ bật 2 Storage Node riêng biệt ở cổng 8001 và 8002
STORAGE_NODES = [
    "http://localhost:8001",
    "http://localhost:8002"
]

def get_node_client(key):
    # Thuật toán phân mảnh: Modulo Hashing
    # Băm chuỗi 'key' thành số nguyên, sau đó chia lấy dư cho tổng số Node
    node_index = hash(key) % len(STORAGE_NODES)
    node_url = STORAGE_NODES[node_index]
    
    print(f"[Proxy] Đã băm khóa '{key}' -> Chuyển hướng tới Node: {node_url}")
    return xmlrpc.client.ServerProxy(node_url)

def set_key(key, value):
    client = get_node_client(key)
    return client.set(key, value)

def get_key(key):
    client = get_node_client(key)
    return client.get(key)

# Khởi chạy Proxy Server ở một cổng duy nhất (Port 8000) để Client giao tiếp
proxy_server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
proxy_server.register_function(set_key, "set")
proxy_server.register_function(get_key, "get")

print("[*] Central Proxy Router đang chạy tại http://localhost:8000")
print("[*] Sẵn sàng điều phối dữ liệu tới các Node...")
proxy_server.serve_forever()