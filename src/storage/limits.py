from falcon_limiter import AsyncLimiter
from falcon_limiter.utils import get_remote_addr

limiter = AsyncLimiter(key_func=get_remote_addr, default_limits='60 / minute')

def Limiter():
    return limiter.middleware