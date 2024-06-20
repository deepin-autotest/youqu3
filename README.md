<p align="center">
  <a href="https://github.com/funny-dream/youqu3">
    <img src="./docs/assets/logo.png" width="100" alt="YouQu3">
  </a>
</p>
<p align="center">
    <em>YouQu3, Next generation Linux automation testing framework.</em>
</p>


--------------

文档：https://youqu.uniontech.com/v3/

--------------

**YouQu3** 是下一代 Linux 自动化测试框架，在继承 YouQu2 诸多亮点功能的同时解决其遇到的问题，同时对各功能进行插件化、模块化改造，全面优化框架接口调用机制。

## [特性]()

- 以 Python 包的形式提供框架能力，方便安装、更新。
- 自带虚拟环境管理器，支持离线部署，用例整体打包交付之后，可以在无网络环境下直接运行。
- 极致轻量化、可定制化依赖，可以根据测试项目类型安装对应的依赖。
- 功能可插拔，以插件的形式提供功能，不安装插件的情况下框架也能正常运行。
- 可视化配置，在浏览器中输入一些配置后即可驱动测试用例执行，搭配远程执行功能，可实现群控测试机执行。
- 支持非开发者下运行，简化系统环境部署。

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

## [YouQu3插件生态]()

| 序号                                  | 插件名称                                              | 说明                                 |
| :----------------------------------------------------------: | ------------------------------------ | ------------------------------------ |
| 1 | [youqu-dogtail](https://github.com/funny-dream/youqu-dogtail) | 属性定位插件                         |
| 2 | [youqu-imagecenter-rpc](https://github.com/funny-dream/youqu-imagecenter-rpc) | 基于 RPC 服务的图像识别插件      |
| 3 | [youqu-mousekey](https://github.com/funny-dream/youqu-mousekey) | 键鼠操作插件                         |
| 4 | [youqu-dbus](https://github.com/funny-dream/youqu-dbus) | D-Bus 操控插件 |
| 5 | youqu-pms-driver | PMS 测试单驱动插件 |
| 6 | [youqu-button-center](https://github.com/funny-dream/youqu-button-center) | 相对位移定位插件 |
| 7 | [pytest-mark-manage](https://github.com/funny-dream/pytest-mark-manage) | 用例标签化管理插件 |
| 8 | [pytest-youqu-playwright](https://github.com/funny-dream/pytest-youqu-playwright) | 基于 Playwright 的 Web UI 自动化插件 |
| 9 | [youqu-html](https://github.com/funny-dream/youqu-html) | YouQu Html Report |
| 10 | [pytest-record-video](https://github.com/funny-dream/pytest-record-video) | 用例失败录屏插件 |
| 11 | [funnylog](https://linuxdeepin.github.io/funnylog/)          | 全自动日志插件                       |
| 12 | [pdocr-rpc](https://linuxdeepin.github.io/pdocr-rpc/)        | 基于 RPC 服务的 OCR 识别插件         |
| 13 | [wdotool](https://github.com/funny-dream/wdotool) | Wayland 下完美的键鼠工具 |

## [UOS测试套件]()

| 序号 | 套件名称                                                     | 说明                       |
| :--: | ------------------------------------------------------------ | -------------------------- |
|  1   | [uos-method-toolkit](https://github.com/funny-dream/uos-method-toolkit)（UMTK ） | UOS 自动化测试操作方法套件 |
|  2   | [uos-case-v20](https://github.com/funny-dream/uos-case-v20)  | UOS 自动化测试操作用例     |

