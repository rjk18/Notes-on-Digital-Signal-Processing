# 2_2_从 FS 到 FT：周期的极限与频谱的连续化

## 1. 核心思想：周期的“拉伸”

从周期信号到非周期信号，本质上是令周期 $T_0 \to \infty$。此时，相邻脉冲被拉向无穷远，离散的谱线最终“挤压”并连成一条连续的曲线。

## 2. 从 FS 复指数形式出发

对于一个周期为 $T_0$ 的周期信号 $\tilde{x}(t)$，其复指数形式的傅里叶级数定义为：

$$
\tilde{x}(t) = \sum_{k=-\infty}^{\infty} X(jk\Omega_0) e^{jk\Omega_0 t} \quad \text{}
$$

其中系数（频谱值）为：

$$
X(jk\Omega_0) = \frac{1}{T_0} \int_{-T_0/2}^{T_0/2} \tilde{x}(t) e^{-jk\Omega_0 t} dt \quad \text{}
$$

## 3. 引入周期无限大的极限过程

当我们将周期 $T_0 \to \infty$ 时，原本的周期信号 $\tilde{x}(t)$ 就变成了非周期信号 $x(t)$。此时会发生三个关键变化：

- **基频趋于无穷小**：基波角频率 $\Omega_0 = \frac{2\pi}{T_0}$ 变为无穷小量，记作 $d\Omega$。
- **谐波频率变为连续变量**：离散的频率点 $k\Omega_0$ 逐渐靠拢，演变为连续的频率变量 $\omega$。
- **求和变为积分**：由于谱线间隔趋于零，级数中的累加 $\sum$ 演变为对整个频率轴的积分 $\int$。

## 4. 定义傅里叶变换（FT）

为了处理 $T_0 \to \infty$ 时系数 $X(jk\Omega_0)$ 趋于零的问题，我们定义**频谱密度函数**（即傅里叶变换）：

$$
X(j\Omega) = \lim_{T_0 \to \infty} X(jk\Omega_0) \cdot T_0 = \int_{-\infty}^{\infty} x(t) e^{-j\Omega t} dt \quad \text{}
$$

## 5. 最终公式推导

将上述变换代回 FS 的合成公式中：

1. 用 $\frac{X(j\Omega)}{T_0}$ 替换 $X(jk\Omega_0)$。
2. 由 $\Omega_0 = \frac{2\pi}{T_0}$ 得 $\frac{1}{T_0} = \frac{\Omega_0}{2\pi} = \frac{d\Omega}{2\pi}$。

代入合成式：

$$
x(t) = \lim_{T_0 \to \infty} \sum_{k=-\infty}^{\infty} {\left( \frac{1}{T_0} X(jk\Omega_0) \right)} e^{jk\Omega_0 t}= \lim_{T_0 \to \infty} \sum_{k=-\infty}^{\infty} X(jk\Omega_0) e^{jk\Omega_0 t} \frac{\Omega_0}{2\pi}
$$

 当 $T_0 \to \infty$ 时：
   * 离散频率 $k\Omega_0$ 变为连续变量 $\Omega$。
   * 频率间隔 $\Omega_0$ 变为微分算子 $d\Omega$。
   * 求和 $\sum_{k=-\infty}^{\infty} (\cdots) \Omega_0 转化为积分 \int_{-\infty}^{\infty} (\cdots)  d\Omega$

最终得到**傅里叶反变换IFT**公式：

$$
x(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} X(j\Omega) e^{j\Omega t} d\Omega \quad \text{}
$$

## 6. 用图像理解“离散到连续”的过程

上面是严格推导。但真正理解这个过程，需要一个直观画面：

* **时域**：脉冲逐渐远离 $\to$ 周期 $T_0$ 变大。
* **频域**：谱线越来越密 $\to$ 间隔 $\Omega_0$ 缩小。
* **最终**：谱线消失，连成连续包络。

下面这张图，展示的正是这个“拉伸”的动态过程：

<p align="center">
    <img src="/images/2_2_从 FS 到 FT：周期的极限与频谱的连续化/2_2_FS到FT演变.gif" width="600" alt="Aliasing Demo Image 2">
</p>

**观察重点:**

1. **谱线间距如何缩小？**（对应 $\Omega_0 = 2\pi/T_0$）
2. **单条谱线高度如何下降？**（单条谱线 $X(jk\Omega_0)$ 的值变小，但图像上保持不变，这是因为 $X(jk\Omega_0)$ 乘上了 $T_0$后，方便观察)
3. **包络是否保持不变？**（虽然单条谱线在变，但谱线的**包络线形状**始终由单周期内的信号波形决定）


## 总结

- **FS** 处理的是周期信号，频谱是离散的“**谱线**”。
- **FT** 处理的是非周期信号，频谱是连续的“**密度函数**”。
- **物理直观**：随着周期 $T_0$ 变大，谱线间隔 $\Omega_0$ 越来越密，最终在极限处连成一片，形成了连续的频谱包络。
