<p align="center">
  <a href="https://github.com/funny-dream/youqu3">
    <img src="./docs/assets/logo.png" width="100" alt="YouQu3">
  </a>
</p>
<p align="center">
    <em>YouQu3, Next generation Linux automation testing framework.</em>
</p>


--------------

**文档：https://funny-dream.github.io/youqu3/**

--------------

**YouQu3** 旨在成为下一代 Linux 自动化测试框架，全新的插件化及模块化功能，带来全新的使用效果。

## [特性]()

- 支持离线部署
- 极致轻量化、可定制化依赖
- 功能可插拔
- 可视化驱动配置
- 支持非开发者下运行
- 命令行友好

## [安装]()

基础环境（默认支持命令行自动化测试）：

```shell
pip install youqu3
```

桌面 UI 自动化测试：

```shell
pip install youqu3[desktop-ui]
```

Web UI 自动化测试：

```shell
pip install youqu3[webui]
```

D-Bus 接口自动化测试：

```shell
pip install youqu3[dbus]
```

HTTP 接口自动化测试：

```shell
pip install youqu3[http]
```

## [YouQu3 插件生态]()

| 序号                                  | 插件名称                                              | 说明                                 | 可用                             |
| :----------------------------------------------------------: | ------------------------------------ | ------------------------------------ | :----------------------------------: |
| 1 | [youqu-dogtail](https://github.com/funny-dream/youqu-dogtail) | 属性定位插件                         | ✔️ |
| 2 | [youqu-imagecenter-rpc](https://github.com/funny-dream/youqu-imagecenter-rpc) | 基于 RPC 服务的图像识别插件      | ✔️ |
| 3 | [youqu-mousekey](https://github.com/funny-dream/youqu-mousekey) | 键鼠操作插件                         | ✔️ |
| 4 | [youqu-dbus](https://github.com/funny-dream/youqu-dbus) | D-Bus 操控插件 | ✔️ |
| 5 | youqu-pms-driver | PMS 测试单驱动插件 | - |
| 6 | youqu-json-report | JSON 测试报告插件 | - |
| 7 | [youqu-button-center](https://github.com/funny-dream/youqu-button-center) | 相对位移定位插件 | ✔️ |
| 8 | youqu-remote-control | 远程交互式控制插件 | - |
| 9 | [pytest-mark-manage](https://github.com/funny-dream/pytest-mark-manage) | 用例标签化管理插件 | ✔️ |
| 10 | [pytest-youqu-playwright](https://github.com/funny-dream/pytest-youqu-playwright) | 基于 Playwright 的 Web UI 自动化插件 | ✔️ |
| 11 | pytest-record-video | 用例失败录屏插件 | - |
| 12 | [funnylog](https://linuxdeepin.github.io/funnylog/)          | 全自动日志插件                       | ✔️ |
| 13 | [pdocr-rpc](https://linuxdeepin.github.io/pdocr-rpc/)        | 基于 RPC 服务的 OCR 识别插件         | ✔️ |
| 14 | [allure-custom](https://github.com/funny-dream/allure-custom) | 基于 Allure 定制的测试报告 | ✔️ |
| 15 | [wdotool](https://github.com/funny-dream/wdotool) | Wayland 下完美的键鼠工具 | - |

## [用例 Demo]()

https://github.com/funny-dream/youqu3-testcase-demo
