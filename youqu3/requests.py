
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

if HAS_REQUESTS is False:
    raise ImportError("requests module is required, try 'pip install requests'")