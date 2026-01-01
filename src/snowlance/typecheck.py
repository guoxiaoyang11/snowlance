import inspect


def typecheck(func):
    sig = inspect.signature(func)

    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        for name, value in bound_args.arguments.items():
            expected_type = func.__annotations__.get(name)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(
                    f"'{name}' must be {expected_type}, got '{type(value)}'"
                )
        return func(*args, **kwargs)

    return wrapper


if __name__ == "__main__":

    @typecheck
    def test(a: int, b: str, c: int | str):
        pass

    test(1, "1", 1)
