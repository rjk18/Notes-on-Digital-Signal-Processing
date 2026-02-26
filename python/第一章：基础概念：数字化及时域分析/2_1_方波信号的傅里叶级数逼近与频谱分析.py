import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 配置中文字体 ---
# 自动尝试加载常用中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

# --- 参数设置 ---
tau = 2  # 矩形脉冲宽度
T0 = 8  # 信号周期
omega0 = 2 * np.pi / T0  # 基波角频率
t = np.linspace(-4, 12, 1000)
omega_limit = 15  # 频率显示范围 (rad/s)

# --- 准备画布 ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.4)

# 1. 时域图表配置
line_time, = ax1.plot([], [], 'b-', lw=1.5, label='傅里叶级数逼近')
ax1.set_ylim(-0.4, 1.4)
ax1.set_xlim(t[0], t[-1])
ax1.set_title('时域：信号合成与吉布斯现象 (Gibbs Phenomenon)')
ax1.set_xlabel('时间 (t)')
ax1.set_ylabel('信号幅度')
ax1.axhline(0, color='black', lw=1)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper right')

# 2. 频域图表配置
omega_cont = np.linspace(-omega_limit, omega_limit, 500)
# 计算连续傅里叶变换 (FT) 包络线 (Sinc 函数)
envelope = (tau / T0) * np.sinc(omega_cont * tau / (2 * np.pi))
ax2.plot(omega_cont, envelope, 'r--', alpha=0.4, label='FT 包络线 (Sinc 函数)')

ax2.set_ylim(-0.2, 0.6)
ax2.set_xlim(-omega_limit, omega_limit)
ax2.set_title('频域：离散谱线与连续包络线的关系')
ax2.set_xlabel(r'角频率 ($\omega$)')
ax2.set_ylabel('幅度')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='upper right')


def update(N):
    # --- 时域：累加谐波 ---
    # 直流分量 X(j0)
    x_approx = tau / T0
    for k in range(1, N + 1):
        # 傅里叶系数 X_k
        X_k = (tau / T0) * np.sinc(k * omega0 * tau / (2 * np.pi))
        # 累加余弦项：2 * X_k * cos(k * omega0 * t)
        x_approx += 2 * X_k * np.cos(k * omega0 * t)

    line_time.set_data(t, x_approx)
    ax1.set_ylabel(f'叠加谐波次数 N = {N}')

    # --- 频域：更新离散谱线 (FS 系数) ---
    # 清除旧的抽样线
    for artist in ax2.containers:
        artist.remove()

    k_vals = np.arange(-N, N + 1)
    omegas = k_vals * omega0
    coeffs = (tau / T0) * np.sinc(omegas * tau / (2 * np.pi))

    # 绘制当前的离散谱，设置 label 以防图例消失
    new_stem = ax2.stem(omegas, coeffs, basefmt=" ", linefmt='g-', markerfmt='go', label='FS 离散系数')

    return line_time, new_stem


# 创建动画 (谐波次数从 1 逐渐增加到 60)
# interval=150 表示每帧间隔 150 毫秒
ani = FuncAnimation(fig, update, frames=np.arange(1, 61), interval=150, blit=False)

# --- 保存动画 ---
# 1. 保存为 GIF (推荐，兼容性好)
print("正在生成 GIF，请稍候...")
ani.save('2_1_傅里叶级数逼近.gif', writer='pillow', fps=10)
print("GIF 保存成功：2_1_傅里叶级数逼近.gif")

# 2. 或者保存为 MP4 (需要安装 FFmpeg)
# ani.save('fourier_series_animation.mp4', writer='ffmpeg', fps=15)

# 如果你仍然想在保存后查看图形，可以保留 plt.show()
plt.show()