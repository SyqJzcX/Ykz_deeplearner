# LearningAnything——基于 VS Code Dev Containers 的深度学习环境搭建

## 1. 容器环境

本容器中构建了以下工具：

1. Ubuntu 22.04
2. cuda 12.6.3（要小于宿主机 CUDA Version: 12.7）
3. cudnn8
4. conda（Python 12.4（管理 Python 虚拟环境）
5. Pytorch 12.6（要小于cuda版本）

## 2. Vscode 插件（可以在 devcontainer.json 中自动配置）

- Docker
- Remote Development
- Pylance
- Python
- autopep8
- Jupyter
- Chinese (Simplified) (简体中文)

## 3. 容器工作目录

事先准备：安装配置`Docker`与`Vscode`。

进入`doc_ml_env`目录构建容器：

在`Vscode`中按下`Ctrl + Shift + P`进入命令面板，点击`Dev Containers:Reopen in Container`构建容器。

构建完成后，与`doc_ml_env`同级的所有目录都在`\workspaces`中，可根据需要自行添加其他项目目录。

进入`\workspaces\doc_ml_env`目录，运行`python test.py`可以验证`Pytorch`的安装与显卡情况。
  
## 4. 项目结构

```text
doc_ml_env
    |    main.ipynb
    |    README.md  # 关于 requirents.txt 的用法
    |    requirements.txt  # 相关依赖
    |    test.py  # 测试 Pytorch 版本与显卡信息
    |    trainer.py  # 模型训练基类
    |    
    └────.devcontainer
            devcontainer.json
            Dockerfile
```

## 5. 目录挂载

- 目录挂载：
  - 这里我们将该目录作为容器的启动目录，将该容器的父目录 \docproj 作为工作区，挂载到容器中的 \workspaces 中
  - 这样可以向容器中加入其他目录目录，整体结构如下所示

```text
workspaces
    └──── doc_cmake_proj  # C/C++ 项目配置  
    |     ... ...  # 其他项目目录     
    └──── doc_ml_env  # 容器启动目录
```

- 这样，通过当前工作区进入容器后，通过code命令即可打开其他项目目录

## 6. 容器构建参数

- 通过`.devcontainer/devcontainer.json`配置。
  - name：容器名
  - image：镜像名与标签
  - runArgs：运行容器的参数
    - shm-size：共享内存大小，根据算力设置
  - build：构建镜像的配置
    - context：构建容器的上下文（.devcontainer 目录的父目录）
    - dockerfile：指定构建容器的 Dockerfile
    - args：构建镜像的参数
      - IMAGE_NAME：指定镜像名称
      - IMAGE_TAG：指定镜像标签，其中指定了 Linux OS 的发行版、G++、Anaconda、Pytorch 等依赖工具的版本
      - ANACONDA_FILE：指定anaconda安装包
      - BASE_IMAGE_TAG：基础镜像标签参数
  - mounts：挂载本地目录
  - customizations
    - vscode
      - extensions：安装容器中需要的 Vscode 扩展

- 两个重要的参数：
  - ANACONDA_FILE：`anaconda`的`shell`安装脚本，需要配置到项目目录下的`install`目录中
  - BASE_IMAGE_TAG：基础镜像`nvdia/cuda`的标签，其中指定了 Linux OS 的发行版、cuDNN、CUDA 等依赖工具的版本
