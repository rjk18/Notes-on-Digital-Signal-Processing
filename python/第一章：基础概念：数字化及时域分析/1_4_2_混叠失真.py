"""
数字信号处理混叠现象演示
作者：一枝一卒 (ID: 一枝一卒)
博客链接：https://github.com/rjk18/Notes-on-Digital-Signal-Processing

说明：本代码演示奈奎斯特-香农采样定理和混叠失真现象
     通过调整参数fs，f1, f2, f_draw等，可以直观观察不同频率信号在不同采样率下的表现
     fs: 100hz,采样频率
     f1：1hz,低频信号
     f2：99hz,高频信号
     f_draw: 1000hz，高分辨率时间向量,绘制图像时候使信号更平滑
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import zhplot

# 设置参数 - 增加采样点使信号更平滑
f_draw= 1000
t_high_res = np.linspace(0, 1, f_draw, endpoint=False)  # 高分辨率时间向量
fs = 100
t_low_res = np.linspace(0, 1, fs, endpoint=False)  # 用于演示采样）

# 创建信号
f1 = 1    # 低频信号 (Hz)
f2 = 99   # 高频信号 (Hz)

# 生成高质量的正弦信号
signal_low_continuous = np.sin(2 * np.pi * f1 * t_high_res)
signal_high_continuous = np.sin(2 * np.pi * f2 * t_high_res)

# 采样后的信号
signal_low_sampled = np.sin(2 * np.pi * f1 * t_low_res)
signal_high_sampled = np.sin(2 * np.pi * f2 * t_low_res)

# 修正的混叠信号计算
fs_low = 100  # 低采样率
nyquist = fs_low / 2  # 奈奎斯特频率

# 计算混叠频率
f_mod = f2 % fs_low  # 对采样率取模
if f_mod > nyquist:
    f_alias = fs_low - f_mod
    phase = np.pi  # 需要相位反转
else:
    f_alias = f_mod
    phase = 0  # 不需要相位反转

signal_alias = np.sin(2 * np.pi * f_alias * t_high_res + phase)

# 创建更美观的图形
plt.figure(figsize=(15, 10))

# 1. 原始低频信号（高质量显示）
plt.subplot(3, 1, 1)
plt.plot(t_high_res, signal_low_continuous, 'b-', linewidth=2, label=f'连续正弦波 {f1}Hz')
plt.plot(t_low_res, signal_low_sampled, 'ro', markersize=4, label='采样点')
for i in range(len(t_low_res)):
    plt.plot([t_low_res[i], t_low_res[i]], [0, signal_low_sampled[i]], 'r--', alpha=0.3)
plt.xlabel('时间 (s)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('低频正弦信号 (不会发生混叠)')

# 2. 原始高频信号
plt.subplot(3, 1, 2)
plt.plot(t_high_res, signal_high_continuous, 'r-', linewidth=2, label=f'连续正弦波 {f2}Hz')
plt.plot(t_low_res, signal_high_sampled, 'ro', markersize=4, label='采样点')
for i in range(len(t_low_res)):
    plt.plot([t_low_res[i], t_low_res[i]], [0, signal_high_sampled[i]], 'r--', alpha=0.3)
plt.xlabel('时间 (s)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('高频正弦信号 (采样频率不足时会发生混叠)')

# 3. 混叠现象演示
plt.subplot(3, 1, 3)
plt.plot(t_high_res, signal_alias, 'g-', linewidth=2, label=f'混叠后感知为 {f_alias}Hz 信号')
plt.plot(t_low_res, signal_high_sampled, 'ro', markersize=4, label='实际采样点')
for i in range(len(t_low_res)):
    plt.plot([t_low_res[i], t_low_res[i]], [0, signal_high_sampled[i]], 'r--', alpha=0.3)
plt.xlabel('时间 (s)')
plt.ylabel('幅度')
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('混叠失真：高频信号被错误解释为低频信号')


plt.tight_layout()
plt.show()