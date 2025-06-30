import torch
import sys


'''
===== Python 版本信息 =====
Python version: 3.11.12

===== PyTorch GPU 信息 =====
CUDA 是否可用: True

可用的GPU数量: 1

=== GPU 0 ===
名称: NVIDIA GeForce RTX 3060 Laptop GPU
总内存: 6.00 GB
多处理器数量: 30
计算能力: 8.6

===== GPU 功能测试 =====

=== GPU 操作测试 ===
张量所在设备: cuda:0
GPU 计算成功！

===== 最终状态 =====
GPU 是否可用: True
GPU 是否可用: True
PyTorch 版本: 2.7.0+cu126
'''

a = [1,23,4,5,.4]
def print_gpu_info():
    # 检查CUDA是否可用
    cuda_available = torch.cuda.is_available()
    print(f"CUDA 是否可用: {cuda_available}")
    
    if not cuda_available:
        return
    
    # 获取GPU数量
    device_count = torch.cuda.device_count()
    print(f"\n可用的GPU数量: {device_count}")
    
    # 打印每个GPU的详细信息
    for i in range(device_count):
        print(f"\n=== GPU {i} ===")
        print(f"名称: {torch.cuda.get_device_name(i)}")
        prop = torch.cuda.get_device_properties(i)
        print(f"总内存: {prop.total_memory / 1024**3:.2f} GB")
        print(f"多处理器数量: {prop.multi_processor_count}")
        print(f"计算能力: {prop.major}.{prop.minor}")

def test_gpu_operation():
    # 尝试在GPU上执行操作
    if torch.cuda.is_available():
        try:
            # 创建测试张量
            x = torch.randn(3, 3).cuda()
            y = torch.randn(3, 3).cuda()
            z = x + y  # 执行GPU计算
            
            # 验证设备类型
            print("\n=== GPU 操作测试 ===")
            print(f"张量所在设备: {x.device}")
            print("GPU 计算成功！")
            return True
        except Exception as e:
            print(f"\nGPU 操作失败: {str(e)}")
            return False
    else:
        print("没有可用的GPU进行测试")
        return False

if __name__ == "__main__":
    print("===== Python 版本信息 =====")
    print(f"Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    print("\n===== PyTorch GPU 信息 =====")
    print_gpu_info()
    
    print("\n===== GPU 功能测试 =====")
    test_result = test_gpu_operation()
    
    print("\n===== 最终状态 =====")
    print(f"GPU 是否可用: {torch.cuda.is_available()}")
    print(f"GPU 是否可用: {test_result}")
    print(f"PyTorch 版本: {torch.__version__}")
