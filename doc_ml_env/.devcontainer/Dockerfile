# FROM 前的标签不能在 FROM 之后用
ARG BASE_IMAGE_TAG=12.6.3-cudnn-devel-ubuntu22.04
# CUDA基础镜像（完整标签由构建参数动态指定）
FROM nvidia/cuda:${BASE_IMAGE_TAG} AS base-system

# Ubuntu 系统环境配置
# 强制系统自动选择默认选项，避免因需要用户输入而使进程卡住
ENV DEBIAN_FRONTEND=noninteractive \
    # 设置时区环境变量
    TZ=Asia/Shanghai \
    # 设置容器字符编码和区域环境
    LANG=C.UTF-8

# 设置代理地址（如果需要）
ARG PROXY_URL=http://host.docker.internal:26561
ARG NO_PROXY=localhost,*.docker.internal

ENV http_proxy=${PROXY_URL} \
    https_proxy=${PROXY_URL} \
    no_proxy=${NO_PROXY}

# 设置代理证书文件名（如果需要）
ARG PROXY_CRT=steamcrt.cer
# 如果需要代理证书复制到容器中
COPY ${PROXY_CRT} /usr/local/share/ca-certificates/${PROXY_CRT}.crt
# 安装 ca-certificates
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    ca-certificates && \
    # 更新 CA 证书
    update-ca-certificates

# 把 Ubuntu 系统的软件源替换成阿里云镜像源
RUN sed -i 's|http://archive.ubuntu.com|http://mirrors.aliyun.com|g' /etc/apt/sources.list && \
    sed -i 's|http://security.ubuntu.com|http://mirrors.aliyun.com|g' /etc/apt/sources.list

# 更新 apt，配置 Python 环境，安装其他依赖（-q 表示安静输出，-qq 更安静）
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    # 配置 C/C++ 开发环境
    # 基础开发工具（包含 gcc、g++、make 等）
    build-essential \
    cmake \
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
    # 添加 deadsnakes PPA：允许安装最新的 Python 版本（如 3.11），同时保留系统 Python 3.8
    # add-apt-repository ppa:deadsnakes/ppa -y && \
    # 清理软件源索引缓存与已下载的安装包文件，减小镜像体积
    apt-get clean && rm -rf /var/lib/apt/lists/*

FROM base-system AS conda-environment

# conda 安装程序名称
ARG CONDA_FILE=Miniconda3-py313_25.5.1-1-Linux-x86_64.sh
# Miniconda 安装脚本的下载地址
ARG CONDA_URL=https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/

# 联网下载并安装 Miniconda
RUN wget ${CONDA_URL}${CONDA_FILE} -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# 本地下载安装
# 将本地下载的 Miniconda 安装脚本复制到镜像中
# COPY ./install/${CONDA_FILE} /tmp/${CONDA_FILE}

# 使用本地脚本安装 Miniconda
# RUN bash /tmp/${CONDA_FILE} -b -p /opt/conda && \
#     # 安装后删除脚本
#     rm /tmp/${CONDA_FILE}

# 设置环境变量，使 Miniconda 的 bin 目录在 PATH 中
ENV PATH=/opt/conda/bin:$PATH

# 设置 conda 的 Python 成为系统默认 Python3
RUN update-alternatives --install /usr/bin/python3 python3 /opt/conda/bin/python3 100 && \
    update-alternatives --set python3 /opt/conda/bin/python3 && \
    # 设置 pip3 源为阿里源
    pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip3 config set install.trusted-host mirrors.aliyun.com

FROM conda-environment AS final-image

# 镜像元数据
# ARG IMAGE_NAME=learn-anything
# ARG IMAGE_TAG=v4.0-pytorch2.7-py313-gpp15-cu129
# LABEL org.opencontainers.image.title=${IMAGE_NAME} \
    # org.opencontainers.image.version=${IMAGE_TAG}

# 安装常用机器学习与数据科学工具
RUN pip3 install --no-cache-dir \
    torch \
    torchvision \
    torchaudio \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    scikit-learn \
    scipy \
    jupyterlab \
    ipywidgets \
    tqdm \
    tensorboard

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
