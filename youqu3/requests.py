
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False