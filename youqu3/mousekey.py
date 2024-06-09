try:
    from youqu_mousekey import MouseKey as MouseKey

    HAS_MOUSEKEY = True
except ImportError:
    HAS_MOUSEKEY = False


class MouseKeyChainMixin:

    x = None
    y = None

    @classmethod
    def _check_xy(cls):
        if cls.x is None and cls.y is None:
            raise ValueError

    @classmethod
    def click(cls):
        cls._check_xy()
        MouseKey.click(cls.x, cls.y)
        return cls

    @classmethod
    def right_click(cls):
        cls._check_xy()
        MouseKey.right_click(cls.x, cls.y)
        return cls

    @classmethod
    def double_click(cls):
        cls._check_xy()
        MouseKey.double_click(cls.x, cls.y)
        return cls

    @classmethod
    def center(cls):
        cls._check_xy()
        return cls.x, cls.y