try:
    from youqu_mousekey import MouseKey as MouseKey

    HAS_MOUSEKEY = True
except ImportError:
    HAS_MOUSEKEY = False

if HAS_MOUSEKEY is False:
    raise ImportError("youqu-mousekey module is required, try 'pip install youqu-mousekey'")
