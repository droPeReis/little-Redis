import time
import threading
from collections import defaultdict

class MemoryStore:
    def __init__(self):
        self._data: dict = {}
        self._expires: dict = {}
        self._lock = threading.RLock()
        self._start_cleanup_worker()

    def _is_expired(self, key: str) -> bool:
        exp = self._expires.get(key)
        return exp is not None and time.time() > exp

    def _delete_if_expired(self, key: str) -> bool:
        if self._is_expired(key):
            self._data.pop(key, None)
            self._expires.pop(key, None)
            return True
        return False

    def _start_cleanup_worker(self):
        def cleanup():
            while True:
                time.sleep(1)
                with self._lock:
                    expired = [k for k in list(self._expires) if self._is_expired(k)]
                    for k in expired:
                        self._data.pop(k, None)
                        self._expires.pop(k, None)

        t = threading.Thread(target=cleanup, daemon=True)
        t.start()

    def _get_live(self, key: str):
        self._delete_if_expired(key)
        return self._data.get(key)


    def set(self, key: str, value: str, ex: int = None):
        with self._lock:
            self._data[key] = value
            if ex is not None:
                self._expires[key] = time.time() + ex
            else:
                self._expires.pop(key, None)
        return "OK"

    def get(self, key: str):
        with self._lock:
            val = self._get_live(key)
            if val is None:
                return None
            if not isinstance(val, str):
                raise TypeError("WRONGTYPE")
            return val

    def delete(self, *keys: str) -> int:
        with self._lock:
            count = 0
            for key in keys:
                if key in self._data and not self._is_expired(key):
                    count += 1
                self._data.pop(key, None)
                self._expires.pop(key, None)
            return count

    def exists(self, key: str) -> bool:
        with self._lock:
            return self._get_live(key) is not None

    def expire(self, key: str, seconds: int) -> bool:
        with self._lock:
            if self._get_live(key) is None:
                return False
            self._expires[key] = time.time() + seconds
            return True

    def ttl(self, key: str) -> int:
        with self._lock:
            if self._get_live(key) is None:
                return -2  
            exp = self._expires.get(key)
            if exp is None:
                return -1 
            return max(0, int(exp - time.time()))

    def incr(self, key: str) -> int:
        with self._lock:
            val = self._get_live(key) or "0"
            if not isinstance(val, str):
                raise TypeError("WRONGTYPE")
            new_val = int(val) + 1
            self._data[key] = str(new_val)
            return new_val


    def lpush(self, key: str, *values) -> int:
        with self._lock:
            lst = self._get_live(key)
            if lst is None:
                lst = []
                self._data[key] = lst
            if not isinstance(lst, list):
                raise TypeError("WRONGTYPE")
            for v in values:
                lst.insert(0, v)
            return len(lst)

    def rpush(self, key: str, *values) -> int:
        with self._lock:
            lst = self._get_live(key)
            if lst is None:
                lst = []
                self._data[key] = lst
            if not isinstance(lst, list):
                raise TypeError("WRONGTYPE")
            lst.extend(values)
            return len(lst)

    def lrange(self, key: str, start: int, stop: int) -> list:
        with self._lock:
            lst = self._get_live(key)
            if lst is None:
                return []
            if not isinstance(lst, list):
                raise TypeError("WRONGTYPE")
            if stop == -1:
                return lst[start:]
            return lst[start:stop + 1]

    def llen(self, key: str) -> int:
        with self._lock:
            lst = self._get_live(key) or []
            return len(lst)

    def hset(self, key: str, field: str, value: str) -> int:
        with self._lock:
            h = self._get_live(key)
            if h is None:
                h = {}
                self._data[key] = h
            if not isinstance(h, dict):
                raise TypeError("WRONGTYPE")
            is_new = field not in h
            h[field] = value
            return 1 if is_new else 0

    def hget(self, key: str, field: str):
        with self._lock:
            h = self._get_live(key)
            if h is None or not isinstance(h, dict):
                return None
            return h.get(field)

    def hgetall(self, key: str) -> dict:
        with self._lock:
            h = self._get_live(key)
            if h is None:
                return {}
            if not isinstance(h, dict):
                raise TypeError("WRONGTYPE")
            return dict(h)

    def hdel(self, key: str, *fields) -> int:
        with self._lock:
            h = self._get_live(key)
            if h is None:
                return 0
            count = sum(1 for f in fields if h.pop(f, None) is not None)
            return count

    def keys(self, pattern: str = "*") -> list:
        import fnmatch
        with self._lock:
            return [k for k in self._data if not self._is_expired(k)
                    and fnmatch.fnmatch(k, pattern)]

    def flush(self):
        with self._lock:
            self._data.clear()
            self._expires.clear()
        return "OK"
    


    ''' 
    
    def ttl(self, key: str) -> int:
        with self._lock:
            if self._get_live(key) is None:     
                return -2   # COM EXPIRACAO ATIVA
            exp = self._expires.get(key)
            if exp is None:
                return -1  # SEM EXPIRACOA
            return max(0, int(exp - time.time()))

    
    
    
    def lrange(self, key: str, start: int, stop: int) -> list:
        with self._lock:
            lst = self._get_live(key)
            if lst is None:
                return []
            if not isinstance(lst, list):
                raise TypeError("WRONGTYPE")
            # Redis: stop -1 = até o fim
            if stop == -1:
                return lst[start:]
            return lst[start:stop + 1]
    
    '''