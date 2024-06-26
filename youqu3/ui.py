from youqu3.exception import YouQuPluginDependencyError

try:
    from youqu_button_center import ButtonCenter as _ButtonCenter

except ImportError:
    raise YouQuPluginDependencyError("youqu-button-center")

from youqu3.mkmixin import MouseKeyChainMixin


class UI(MouseKeyChainMixin):

    def __init__(
            self,
            appname: str,
            config_path: str,
            number: int = -1,
            pause: int = 1,
            retry: int = 1,
    ):
        self.appname = appname
        self.config_path = config_path
        self.number = number
        self.pause = pause
        self.retry = retry

    def ui(
            self,
            btn_name,
            offset_x=None,
            multiplier_x=None,
            offset_y=None,
            multiplier_y=None,
    ):
        MouseKeyChainMixin.result = _ButtonCenter(
            appname=self.appname,
            config_path=self.config_path,
            number=self.number,
            pause=self.pause,
            retry=self.retry
        ).btn_center(
            btn_name,
            offset_x=offset_x,
            multiplier_x=multiplier_x,
            offset_y=offset_y,
            multiplier_y=multiplier_y,
        )
        if isinstance(self.result, tuple):
            MouseKeyChainMixin.x, MouseKeyChainMixin.y = MouseKeyChainMixin.result
        return self

