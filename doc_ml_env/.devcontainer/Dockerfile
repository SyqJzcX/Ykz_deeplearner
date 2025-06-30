# FROM 前的标签不能在 FROM 之后用
ARG BASE_IMAGE_TAG=12.6.3-cudnn-devel-ubuntu22.04

# CUDA基础镜像（完整标签由构建参数动态指定）
FROM nvidia/cuda:${BASE_IMAGE_TAG}

# 使用参数：镜像名与标签
ARG IMAGE_NAME="learn-anything"
ARG IMAGE_TAG="v3.5-pytorch2.6-conda3.12-gpp11.4-cu126"
ARG ANACONDA_FILE
ARG ANACONDA_URL=https://repo.anaconda.com/archive/${ANACONDA_FILE}

# 为镜像设置标签
LABEL org.opencontainers.image.title="${IMAGE_NAME}"
LABEL org.opencontainers.image.version="${IMAGE_TAG}"

# Ubuntu 系统初始设置
# 强制系统自动选择默认选项，避免因需要用户输入而使进程卡住
ENV DEBIAN_FRONTEND=noninteractive
# 设置时区环境变量
ENV TZ=Asia/Shanghai
# 设置容器字符编码和区域环境
ENV LANG=C.UTF-8

# 把 Ubuntu 系统的软件源替换成阿里云镜像源
RUN sed -i 's|http://archive.ubuntu.com|http://mirrors.aliyun.com|g' /etc/apt/sources.list
RUN sed -i 's|http://security.ubuntu.com|http://mirrors.aliyun.com|g' /etc/apt/sources.list

# 更新 apt，配置 Python 环境，安装其他依赖（-q 表示安静输出，-qq 更安静）
RUN apt update -qq && \
    apt install -y --no-install-recommends software-properties-common && \
    # 添加 deadsnakes PPA：允许安装最新的 Python 版本（如 3.11），同时保留系统 Python 3.8
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt update -qq && \
    apt install -y --no-install-recommends \
    # 配置 C/C++ 开发环境
    # 基础开发工具（包含 gcc、g++、make 等）
    build-essential \
    cmake \
    ninja-build \
    gdb \
    # 替代 make 的高性能构建系统
    ninja-build \
    # Ubuntu 常用
    git \
    curl \
    iproute2 \
    # 通过 URL 获取安装脚本
    wget \
    # 包含 SSL 证书，用于验证 HTTPS 连接的安全性
    ca-certificates && \
    # 清理软件源索引缓存与已下载的安装包文件，减小镜像体积
    apt clean && rm -rf /var/lib/apt/lists/*

# 联网下载并安装Anaconda(太慢了)
# RUN wget ${ANACONDA_URL} -O anaconda.sh && \
#     bash anaconda.sh -b -p /opt/conda && \
#     rm anaconda.sh

# 本地下载安装
# 将本地下载的Anaconda安装脚本复制到镜像中
COPY ./install/${ANACONDA_FILE} /tmp/${ANACONDA_FILE}

# 使用本地脚本安装Anaconda
RUN bash /tmp/${ANACONDA_FILE} -b -p /opt/conda && \
    # 安装后删除脚本
    rm /tmp/${ANACONDA_FILE}

# 设置环境变量，使Anaconda的bin目录在PATH中
ENV PATH=/opt/conda/bin:$PATH

# 设置conda的Python成为系统默认Python3
RUN update-alternatives --install /usr/bin/python3 python3 /opt/conda/bin/python3 100 && \
    update-alternatives --set python3 /opt/conda/bin/python3

# 设置 pip3 源为阿里源
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 config set install.trusted-host mirrors.aliyun.com

# 升级pip：确保使用最新的 pip 版本
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# 安装 PyTorch
RUN pip3 install torch torchvision torchaudio

# 安装 Ollama

# 一键安装：网速太慢
# RUN curl -fsSL https://ollama.com/install.sh | bash

# 下载包
# RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
# 解压到/usr目录
# RUN sudo tar -C /usr -xzf ollama-linux-amd64.tgz

# 设置工作目录（容器中的）
# WORKDIR /workspace

# # 将本地代码复制到容器中
# COPY . /workspace

# 安装额外的依赖（如果有）
# RUN pip3 install --no-cache-dir -r requirements.txt

# 暴露端口（如果有需要）
# EXPOSE 8000

# 定义容器启动时运行的命令
# CMD ["python", "app.py"]
