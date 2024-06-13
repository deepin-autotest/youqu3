---
Author : mikigo
---

# UOS 系统测试套件（UMTK）

## 1. 简介

UOS 系统测试套件（全称：UOS 系统自动化测试操作方法套件，以下简称测试套件）是基于 YouQu3 封装的 UOS 操作系统预装应用的元素操作方法套件。

测试套件是一个独立项目，旨在提供系统预装应用所有的元素的操作方法，这些元素操作方法可以用于自动化用例调用，组装成自动化测试用例。

## 2. 工程设计

### 2.1. 工程结构

```shell
uos-method-toolkit
├── LICENSE
├── README.md
└── umtk
    ├── dde_file_manager
    │   ├── dde_file_manager_method.py
    │   └── __init__.py
    ├── deepin_music
    │   ├── deepin_music_method.py
    │   └── __init__.py
    ├── deepin_movie
    │   ├── deepin_music_method.py
    ... ...
    └── __init__.py
```

### 2.2. 方案说明

- 系统中各应用划分自己的模块，模块名称为应用包名，下划线连接单词。

- 每个应用存在一个唯一的出口文件，供外部用例调用。

  ```python
  from umtk.dde_file_manager import DdeFileManagerMethod
  ```

  `DdeFileManagerMethod` 可以调用  `dde-file-manager` 所有的元素操作方法。

- 所有方法以类的形式编写，遵循 PO 设计模式。

- 测试套件中所有的方法均为原子操作，不做复杂步骤的封装。

## 3. 套件的发布

- 套件分大版本发布，比如 V20、V25 是不同的测试套件版本，在不同的代码仓库中。

- 在同一个大版本中，套件持续保持更新，并在系统关键节点发布对应的版本；

  比如 V20 阶段，1070 发布一个套件版本，1071 发布一个套件版本，一次类推，过程中如果根据需要出小版本。

- 套件通过 PyPI 发布，用户可直接通过 pip 命令安装使用：

  安装：

  ```shell
  pip install umtk
  ```

  使用：

  ```python
  from umtk.dde_file_manager import DdeFileManagerMethod
  ```

## 4. 套件的维护

- 套件由专人主责维护（maintainer），其他人可以提需求或 issue，以保持套件的各方面一致性。

- 鼓励内外部开发者贡献 PR。

## 5. 对套件的测试

套件里面保存元素的操作方法，在操作方法多了之后，维护方法的稳定性有效性将成为一个问题。

因此，我们需要建立对套件的自动化测试，专门针对元素操作方法函数进行测试。