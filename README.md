# 基于 VS Code Dev Containers 的深度学习环境搭建

## 1. 容器构建

进入`doc_ml_env`目录构建容器。
构建完成后，与`doc_ml_env`同级的所有目录都在`\workspaces`中，可根据需要自行添加其他项目目录。

## 2. 容器环境与插件安装

1. Ubuntu 22.04
2. cuda 12.6.3（要小于宿主机 CUDA Version: 12.7）
3. cudnn
4. conda（管理 Python 虚拟环境）
5. Pytorch 12.6（要小于cuda版本）

## 3. Vscode 插件（可以在 devcontainer.json 中自动配置）

- Docker
- Remote Development
- Pylance
- Python
- autopep8
- Jupyter
- C++
- C++ Extension pack
- Chinese (Simplified) (简体中文)
  
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

```txt
workspaces
    └──── doc_cmake_proj  # C/C++ 项目配置  
    |     ... ...  # 其他项目目录     
    └──── doc_ml_env  # 容器启动目录
  - 这样，通过当前工作区进入容器后，通过code命令即可打开其他项目目录
```

## 6. 构建并进入容器环境

- 在 VS Code 中打开项目文件
- 按下【F1】在上方选择【Dev Containers:Reopen in Container】
  - 经历漫长的等待 ... ... （下载基础镜像、执行 Dockerfile 命令）
- 此时查看 vscode 左下角，蓝底白字，显示Dev Container: GPU Development,torch2.5+..，就说明我们现在的项目 torch-test 已经在使用刚才拉取的pytorch容器了！
- 在左边找到app.py，运行他，若显示可用gpu大于0，表示项目torch-test中的python程序可以使用gpu。之后我们需要运行深度学习程序时，使用这里的步骤即可，不需要安装额外的python环境了，若需要安装其他包，那就修改requirements.txt文件即可

## 7. 补充一些可能遇到的其他问题

- 需要安装其他 python 包怎么办？
  - 若我们需要其他 python 包，那就在终端直接安装
  - 测试能用之后，用pip freeze | grep -v '@ file://' > requirements.txt将当前python环境中的包导出到文件requirements.txt中
  - 之后再启动项目时，Dev Container会自动帮我们根据文件requirements.txt安装环境
- 如何重新构建容器
  - 按【F1】，搜索【Dev Containers:Rebuild Container】
- 在镜像中添加VS Code插件：可以在镜像中添加 VS Code 插件，之后每次构建，镜像都会自动安装插件，不用自己手动安装了
  - 右键单击插件，点击【Add to devcontainer.json】
- 目录挂载：
  - 可以将当前工作目录的父目录 \docproj 挂载到容器中的 \workspaces 中，这样可以向容器中加入其他目录
  - 这样，通过当前工作区进入容器后，通过code命令即可打开其他项目目录
