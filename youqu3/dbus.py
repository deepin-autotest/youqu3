from youqu3.exceptions import YouQuPluginDependencyError

try:
    from pydbussend import PyDBusSend as Dbus

    HAS_PYDBUSSEND = True
except ImportError:
    HAS_PYDBUSSEND = False

if HAS_PYDBUSSEND is False:
    raise YouQuPluginDependencyError("pydbussend")
