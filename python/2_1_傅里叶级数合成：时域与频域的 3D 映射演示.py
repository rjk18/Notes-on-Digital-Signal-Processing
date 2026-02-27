
"""
数字信号处理：傅里叶级数合成与“时-频”映射 3D 演示
作者：一枝一卒 (ID: 一枝一卒)
博客链接：https://github.com/rjk18/Notes-on-Digital-Signal-Processing

说明：本代码通过 3D 坐标系可视化周期矩形脉冲的分解与合成过程。
     - X轴 (时间): 展示合成波形 x(t) 及其各次谐波。
     - Y轴 (频率): 将不同频率的谐波在空间上剥离，展示“正交基”的独立性。
     - Z轴 (幅度): 定量展示各次谐波的贡献强度。

物理参数：
     tau = 2    : 矩形脉冲宽度。决定了频域 Sinc 包络的“主瓣宽度”。
     T0 = 8     : 信号周期。决定了离散谱线的间隔 (Ω0)。
     omega0     : 基波角频率 (2π/T0)。
     harmonics  : 谐波次数 (1~6)，用于清晰观察空间层次。
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- 1. 解决中文显示问题 ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'sans-serif'] # 优先使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# --- 参数设置 ---
T0 = 8
omega0 = 2 * np.pi / T0
t = np.linspace(0, 2 * T0, 1000)
harmonics = np.arange(1, 7)  # 显示 1-6 次谐波
tau = 2

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# --- 2. 绘制各个谐波分量 (分层) ---
# 注意：字符串前加 r 以修复 SyntaxWarning: invalid escape sequence '\O'
x_total = np.full_like(t, tau / T0)

for k in harmonics:
    ak = (2 * tau / T0) * np.sinc(k * omega0 * tau / (2 * np.pi))
    y_k = ak * np.cos(k * omega0 * t)
    x_total += y_k
    # y 轴方向代表频率深度
    ax.plot(t, y_k, zs=k, zdir='y', color='royalblue', alpha=0.5, lw=1)

# --- 3. 绘制时域合成信号 (放在最前面 y=0) ---
ax.plot(t, x_total, zs=0, zdir='y', color='red', lw=2.5, label=r'$\tilde{x}(t)$')

# --- 4. 绘制频域谱线 (放在侧面 t=max) ---
k_freq = np.arange(0, 7)
# 幅度计算
amps = [tau/T0] + [(2 * tau / T0) * np.sinc(k * omega0 * tau / (2 * np.pi)) for k in harmonics]

for k, amp in zip(k_freq, amps):
    # 绘制垂直谱线
    ax.plot([t[-1], t[-1]], [k, k], [0, amp], color='navy', lw=1.5)
    ax.scatter(t[-1], k, amp, color='navy', s=20)

# --- 5. 细节修饰 ---
# 使用 r'' 原始字符串彻底解决 \Omega 的报错
ax.set_xlabel('时间 (t)', labelpad=10)
ax.set_ylabel(r'频率 ($k\Omega_0$)', labelpad=10)
ax.set_zlabel('幅度', labelpad=10)

# 设置 y 轴刻度标签
ax.set_yticks(k_freq)
ax.set_yticklabels([rf'${k}\Omega_0$' if k!=0 else '0' for k in k_freq])

# 调整视角：elev是仰角，azim是方位角
ax.view_init(elev=22, azim=-55)

plt.title('傅里叶级数合成：时域与频域的 3D 映射演示')
plt.tight_layout()
plt.savefig('fourier_3d.svg', format='svg', bbox_inches='tight')
plt.show()