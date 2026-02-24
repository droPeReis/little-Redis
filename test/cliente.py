import socket

def send(cmd: str, host="127.0.0.1", port=6380) -> str:
    with socket.socket() as s:
        s.connect((host, port))
        s.sendall((cmd + "\n").encode())
        return s.recv(4096).decode()

# Exemplos
print(send("PING"))                        # +PONG
print(send("SET nome Claude EX 60"))       # +OK
print(send("GET nome"))                    # $6\r\nClaude
print(send("INCR visitas"))               # :1
print(send("LPUSH lista a b c"))          # :3
print(send("LRANGE lista 0 -1"))          # *3...
print(send("HSET user nome Ana"))         # :1
print(send("HGET user nome"))             # $3\r\nAna
print(send("TTL nome"))                   # :59 (ou menos)