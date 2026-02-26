"""
数字信号处理 - 连续信号离散化采样演示
作者：一枝一卒 (ID: 一枝一卒)
博客链接：https://github.com/rjk18/Notes-on-Digital-Signal-Processing

说明：本代码演示连续信号如何通过采样变为离散信号
     展示了时域信号采样过程的完整视图，包括连续波形、采样点和离散序列
     修改参数f、T_s、num_cycles等，观察不同采样率下的信号表示
"""



import numpy as np
import matplotlib.pyplot as plt
import zhplot

# ===================== 1. 参数定义 =====================
f = 1.0  # 频率 (Hz)
T = 1/f  # 周期 (秒)
T_s = T/10  # 采样周期，每个周期10个点

# 时间参数
num_cycles = 1  # 显示的周期数
t_max = num_cycles * T  # 总时间

# 连续时间（用于绘制平滑波形）
t_continuous = np.linspace(0, t_max, 500)  # 500个点用于绘制连续波形

# 离散时间（每个周期10个点）
t_discrete = np.arange(0, t_max, T_s)  # 从0开始，步长为T_s

# 计算信号值
x_continuous = np.sin(2 * np.pi * f * t_continuous)  # 连续信号
x_discrete = np.sin(2 * np.pi * f * t_discrete)      # 离散采样信号

print("=== 信号参数 ===")
print(f"信号频率: f = {f} Hz")
print(f"信号周期: T = {T} 秒")
print(f"采样周期: T_s = {T_s} 秒")
print(f"采样频率: f_s = {1/T_s} Hz")
print(f"总周期数: {num_cycles}")
print(f"总采样点数: {len(t_discrete)}")
print("\n=== 离散采样点 ===")
for i, (t, x) in enumerate(zip(t_discrete, x_discrete)):
    print(f"点 {i:2d}: t = {t:.2f}s, x = {x:.4f}")

# ===================== 2. 创建图形 =====================
fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 5))

# ===================== 3. 左侧子图：连续信号与采样点 =====================
# 绘制连续信号
ax_left.plot(t_continuous, x_continuous, 'b-', linewidth=2,
             label=r'$x_c(t) = \sin(2\pi t)$', alpha=0.7)

# 标记采样点
ax_left.plot(t_discrete, x_discrete, 'ro', markersize=8, label='采样点')

# 绘制采样垂直线
for t, x in zip(t_discrete, x_discrete):
    ax_left.plot([t, t], [0, x], 'r--', alpha=0.5, linewidth=1)

# 标记周期
for n in range(num_cycles + 1):
    t_n = n * T
    ax_left.axvline(x=t_n, color='g', linestyle=':', alpha=0.5, linewidth=1)
    ax_left.text(t_n, 1.1, f'T={n}', ha='center', fontsize=9)

# 设置左侧图
ax_left.set_xlabel(r'时间 $t$ (秒)', fontsize=12)
ax_left.set_ylabel(r'幅度 $x(t)$', fontsize=12)
ax_left.set_title(r'连续信号 $x_c(t) = \sin(2\pi t)$ 与离散采样点', fontsize=14)
ax_left.grid(True, linestyle='--', alpha=0.6)
ax_left.set_ylim(-1.3, 1.3)
ax_left.legend(loc='upper right', fontsize=10)
ax_left.set_xlim(-0.1, t_max + 0.1)

# ===================== 4. 右侧子图：离散信号（stem图） =====================
# 使用stem绘制离散信号
markerline, stemlines, baseline = ax_right.stem(
    t_discrete, x_discrete,
    linefmt='r-',
    markerfmt='ro',
    basefmt='k-',
    label=r'离散信号 $x[n]$'
)
plt.setp(stemlines, 'linewidth', 1.5, 'alpha', 0.7)
plt.setp(markerline, 'markersize', 8)



# 设置右侧图
ax_right.set_xlabel(r'时间 $t$ (秒)', fontsize=12)
ax_right.set_ylabel(r'幅度 $x_s(t)$', fontsize=12)
ax_right.set_title(f'离散采样信号 (采样频率: {1/T_s:.1f} Hz)', fontsize=14)
ax_right.grid(True, linestyle='--', alpha=0.6)
ax_right.set_ylim(-1.3, 1.3)
ax_right.legend(loc='upper right', fontsize=10)
ax_right.set_xlim(-0.1, t_max + 0.1)

# ===================== 5. 添加信息文本 =====================
info_text = f'信号频率: f = {f} Hz\n采样频率: f_s = {1/T_s:.1f} Hz\n采样间隔: T_s = {T_s:.2f} s\n每周期点数: 10'
fig.text(0.02, 0.02, info_text, fontsize=10,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))

# ===================== 6. 显示图形 =====================
plt.tight_layout(rect=[0, 0.05, 1, 0.98])
plt.show()
