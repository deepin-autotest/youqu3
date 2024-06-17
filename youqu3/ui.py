from youqu3.exception import YouQuPluginInstalledError

try:
    from youqu_button_center import ButtonCenter

except ImportError:
    raise YouQuPluginInstalledError("youqu-button-center")