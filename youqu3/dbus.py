from youqu3.exceptions import YouQuPluginDependencyError

try:
    from youqu_dbus import DbusUtils as Dbus

    HAS_YOUQU_DBUS = True
except ImportError:
    HAS_YOUQU_DBUS = False

if HAS_YOUQU_DBUS is False:
    raise YouQuPluginDependencyError("youqu-dbus")
