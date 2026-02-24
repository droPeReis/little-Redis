from store import MemoryStore

store = MemoryStore()

def handle_command(raw: str) -> str:
    parts = raw.strip().split()
    if not parts:
        return "-ERR empty command\r\n"

    cmd = parts[0].upper()
    args = parts[1:]

    try:
        match cmd:
            # Strings
            case "SET":
                ex = int(args[2]) if len(args) >= 3 and args[2].upper() == "EX" and len(args) >= 4 else None
                if len(args) >= 4 and args[2].upper() == "EX":
                    ex = int(args[3])
                return f"+{store.set(args[0], args[1], ex=ex)}\r\n"
            case "GET":
                val = store.get(args[0])
                return f"${len(val)}\r\n{val}\r\n" if val else "$-1\r\n"
            case "DEL":
                return f":{store.delete(*args)}\r\n"
            case "EXISTS":
                return f":{int(store.exists(args[0]))}\r\n"
            case "INCR":
                return f":{store.incr(args[0])}\r\n"
            case "EXPIRE":
                return f":{int(store.expire(args[0], int(args[1])))}\r\n"
            case "TTL":
                return f":{store.ttl(args[0])}\r\n"

            # Listas
            case "LPUSH":
                return f":{store.lpush(args[0], *args[1:])}\r\n"
            case "RPUSH":
                return f":{store.rpush(args[0], *args[1:])}\r\n"
            case "LRANGE":
                items = store.lrange(args[0], int(args[1]), int(args[2]))
                resp = f"*{len(items)}\r\n"
                for item in items:
                    resp += f"${len(item)}\r\n{item}\r\n"
                return resp
            case "LLEN":
                return f":{store.llen(args[0])}\r\n"

            # Hashes
            case "HSET":
                return f":{store.hset(args[0], args[1], args[2])}\r\n"
            case "HGET":
                val = store.hget(args[0], args[1])
                return f"${len(val)}\r\n{val}\r\n" if val else "$-1\r\n"
            case "HGETALL":
                h = store.hgetall(args[0])
                resp = f"*{len(h)*2}\r\n"
                for k, v in h.items():
                    resp += f"${len(k)}\r\n{k}\r\n${len(v)}\r\n{v}\r\n"
                return resp
            case "HDEL":
                return f":{store.hdel(args[0], *args[1:])}\r\n"

            # Utilitários
            case "KEYS":
                pattern = args[0] if args else "*"
                ks = store.keys(pattern)
                resp = f"*{len(ks)}\r\n"
                for k in ks:
                    resp += f"${len(k)}\r\n{k}\r\n"
                return resp
            case "FLUSHALL":
                return f"+{store.flush()}\r\n"
            case "PING":
                return "+PONG\r\n"

            case _:
                return f"-ERR unknown command '{cmd}'\r\n"

    except (IndexError, ValueError):
        return "-ERR wrong number of arguments or invalid value\r\n"
    except TypeError as e:
        return f"-WRONGTYPE {e}\r\n"