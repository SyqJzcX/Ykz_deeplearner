# 基于 CNN 和 CIFAR-10 的图像识别

## 实现任务

见`cnn.ipynb`

## 环境构建

构建容器，见`.devcontainer`

## pip 环境导入导出

从requirements.txt导入环境：
`pip install --no-cache-dir -r requirements.txt`
导出环境到文件requirements.txt：
`pip freeze | grep -v '@ file://' > requirements.txt`
