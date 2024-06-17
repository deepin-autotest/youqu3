from youqu3 import exception

class MouseKeyChainMixin:
    x = None
    y = None
    result = None

    @classmethod
    def _check_xy(cls):
        if cls.x is None and cls.y is None:
            raise exception.ElementNotFound("坐标未找到")

    @classmethod
    def click(cls):
        cls._check_xy()
        from youqu_mousekey import MouseKey
        MouseKey.click(cls.x, cls.y)
        return cls

    @classmethod
    def right_click(cls):
        cls._check_xy()
        from youqu_mousekey import MouseKey
        MouseKey.right_click(cls.x, cls.y)
        return cls

    @classmethod
    def double_click(cls):
        cls._check_xy()
        from youqu_mousekey import MouseKey
        MouseKey.double_click(cls.x, cls.y)
        return cls

    @classmethod
    def center(cls):
        if cls.x is None and cls.y is None:
            return None
        return cls.x, cls.y
