import socket

def send(cmd: str, host="127.0.0.1", port=6380) -> str:
    with socket.socket() as s:
        s.connect((host, port))
        s.sendall((cmd + "\n").encode())
        return s.recv(4096).decode()

# Limpa estado anterior
print("=== FLUSH ===")
print(send("FLUSHALL"))

# Ping
print("=== PING ===")
print(send("PING"))

# SET com EX
print("=== SET com EX ===")
print(send("SET nome Claude EX 60"))
print(send("GET nome"))
print(send("TTL nome"))

# INCR
print("=== INCR ===")
print(send("SET visitas 0"))
print(send("INCR visitas"))
print(send("INCR visitas"))
print(send("GET visitas"))

# Lista
print("=== LISTA ===")
print(send("RPUSH fila a b c"))
print(send("LRANGE fila 0 -1"))
print(send("LLEN fila"))

# Hash
print("=== HASH ===")
print(send("HSET user nome Ana"))
print(send("HGET user nome"))
print(send("HGETALL user"))
