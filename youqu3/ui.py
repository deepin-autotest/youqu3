from youqu3.exception import YouQuPluginInstalledError

try:
    from youqu_button_center import ButtonCenter as _ButtonCenter

except ImportError:
    raise YouQuPluginInstalledError("youqu-button-center")

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

if __name__ == '__main__':
    a = UI(app_name="dde-file-manager", config_path="/home/mikigo/github/youqu3/ui.ini").ui("播放按钮").center()
    print(a)

