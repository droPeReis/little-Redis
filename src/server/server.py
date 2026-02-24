import socket
import threading
from commands import handle_command

HOST = "127.0.0.1"
PORT = 6380  # Porta diferente do Redis real (6379)

def handle_client(conn, addr):
    print(f"[+] Conexão de {addr}")
    with conn:
        buf = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buf += data.decode()
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                response = handle_command(line)
                conn.sendall(response.encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"🟢 Mini-Redis rodando em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()