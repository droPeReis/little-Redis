import socket

def send(cmd: str, host="127.0.0.1", port=6380) -> str:
    with socket.socket() as s:
        s.connect((host, port))
        s.sendall((cmd + "\n").encode())
        return s.recv(4096).decode()

print("=== FLUSH ===")
print(send("FLUSHALL"))

print("=== PING ===")
print(send("PING"))

print("=== SET com EX ===")
print(send("SET nome Claude EX 60"))
print(send("GET nome"))
print(send("TTL nome"))

print("=== INCR ===")
print(send("SET visitas 0"))
print(send("INCR visitas"))
print(send("INCR visitas"))
print(send("GET visitas"))

print("=== LISTA ===")
print(send("RPUSH fila a b c"))
print(send("LRANGE fila 0 -1"))
print(send("LLEN fila"))

print("=== HASH ===")
print(send("HSET user nome Ana"))
print(send("HGET user nome"))
#print(send("HGETALL user"))

'''

    --- ADICIONAR O RESTO

print(send("FLUSHALL"))

print(send("TTL nome"))

print(send("GET visitas"))

print(send("HGETALL user"))


'''