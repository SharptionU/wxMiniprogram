import time
from functools import wraps


def timer(print_args=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start

            if print_args:
                print(
                    f"⏱️ \033[93m计时\033[0m: \033[93m{func.__name__}\033[0m(\033[91margs={args}, kwargs={kwargs}\033[0m) -> \033[92m{duration:.6f}s\033[0m")
            else:
                print(f"⏱️ \033[93m计时\033[0m: \033[93m{func.__name__}\033[0m -> \033[92m{duration:.6f}s\033[0m")

            return result

        return wrapper

    return decorator