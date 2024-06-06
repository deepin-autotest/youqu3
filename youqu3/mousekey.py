try:
    from youqu_mousekey import MouseKey as MouseKey

    HAS_MOUSEKEY = True
except ImportError:
    HAS_MOUSEKEY = False