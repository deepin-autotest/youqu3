# OCR识别

## 元素定位

框架代码示意（Client）：

```python
from src import OCR

OCR.ocr(
    *target_strings, 
    picture_abspath=None, 
    similarity=0.6, 
    return_default=False, 
    return_first=False, 
    lang="ch"
)
```

对于一些文案的场景非常适用，此方法直接返回坐标，可以用于**元素定位**。

```python
from youqu3.ocr import OCR

OCR.ocr("确定").click()
OCR.ocr("确定").center()
OCR.ocr("确定").right_click()
OCR.ocr("确定").double_click()
```

## 断言

也可以用于**文字断言**，代码示意： 

```python
def test_001(self):
    ...
    self.assert_ocr_exist("取消收藏")
```

## 实现原理

RPC 的调用逻辑：

![](https://pic.imgdb.cn/item/64f054c3661c6c8e54ff47b5.png)

这样我们只需要在服务端部署好 OCR 识别的服务，然后通过 RPC 服务将功能提供出来，框架里面只需要调用对应的 RPC 接口就行了。

## 负载均衡

随着 OCR 服务在自动化测试子项目中被广泛使用，单台服务远不能满足业务需求，因此我们需要将 OCR 服务做分布式集群化部署，然后通过负载均衡技术将业务请求分发到 OCR 服务器上。

### 为什么基于 Nginx 的负载均衡方案不能满足业务需求

1. 每次 `OCR` 识别业务实际是两次 `RPC` 接口请求，第 1 次是将当前屏幕截图并发送到 `PRC` 服务器，第 2 次调用识别的接口做识别，采用 Nginx 轮询算法做负载均衡会出现两次 `RPC` 请求被分发到两台不同的服务器上，这明显是错误的。
2. 基于 Nginx `ip_hash` 的 `session` 管理负载均衡算法时，Nginx 默认取 IP 的前 3 段做哈希，而我们的测试机都在同一个网段，IP 前 3 段是一样的，因此会导致负载不均衡。

### YouQu 的解决方案

为了解决上面 2 个问题，YouQu3 在 `ocr` 模块对  [pdocr-rpc](https://linuxdeepin.github.io/pdocr-rpc/) 功能进行了增强，实现了一个中间件用以在用例跑测过程中对 OCR 服务集群进行负载均衡。

![](/指南/可选功能/ocr/youqu-ocr.png)

