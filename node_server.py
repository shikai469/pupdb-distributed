import sys
from xmlrpc.server import SimpleXMLRPCServer
from pupdb_core import PupDB

def start_server(port):
    # Mỗi node sẽ có một file database riêng dựa trên port để không bị trùng lặp
    db_filename = f"pupdb_node_{port}.json"
    db = PupDB(db_filename)

    # Khởi tạo RPC Server lắng nghe trên localhost
    server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
    
    # Đăng ký các hàm của PupDB để client có thể gọi qua mạng
    server.register_function(db.set, "set")
    server.register_function(db.get, "get")
    server.register_function(db.remove, "remove")
    server.register_function(db.keys, "keys")

    print(f"[*] Storage Node đang chạy tại http://localhost:{port}")
    print(f"[*] Dữ liệu được lưu tại file: {db_filename}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Đang tắt server...")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cách sử dụng: python node_server.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    start_server(port)