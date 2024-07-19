#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

class DBus:

    def __init__(
            self,
            service_name: str,
            path: str = None,
            interface: str = None,
    ):
        self.cmd = ["dbus-send"]
        self.cmd.append(f"--dest={service_name}")
        self.cmd.append(f"/{service_name.replace('.', '/')}" if path is None else path)
        self.interface = service_name if interface is None else interface
        self.cmd.append(self.interface)

    @property
    def session(self):
        self.cmd.insert(1, "--session")
        self.cmd.insert(2, "--print-reply=literal")
        return self

    @property
    def system(self):
        self.cmd.insert(1, "--system")
        self.cmd.insert(2, "--print-reply=literal")
        return self

    def method(self, method: str):
        self.cmd.remove(self.interface)
        self.cmd.append(f"{self.interface}.{method}")
        return self

    def string(self, *args: str):
        for arg in args:
            self.cmd.append(f'string:"{arg}"')
        return self

    def int32(self, *args: int):
        for arg in args:
            self.cmd.append(f'int32:{arg}')
        return self

    def bool(self, *args: bool):
        for arg in args:
            self.cmd.append(f'boolean:{str(arg).lower()}')
        return self

    def send(self):
        from youqu3.cmd import Cmd
        return Cmd.run(" ".join(self.cmd))

    def sudo_send(self, password=None):
        from youqu3.cmd import Cmd
        return Cmd.sudo_run(" ".join(self.cmd), password=password)


if __name__ == "__main__":
    DBus(
        service_name="org.kde.KWin",
        path="/Screenshot",
        interface="screenshotFullscreen",
    ).session.send()
