# 2_6_矩阵分解视角下的快速傅里叶变换FFT

## 1. 从 4 点 DFT 看矩阵的稀疏化推导

FFT 的本质是将 $N \times N$ 的稠密矩阵分解为 $\log_2 N$ 个**稀疏矩阵**的乘积。

**阶段 1：原始稠密矩阵 $O(N^2)$** 

对于 $N=4$，DFT 变换矩阵 $\mathbf{W}_4$ 为：

$$
\mathbf{X} = \begin{bmatrix} 
W_4^0 & W_4^0 & W_4^0 & W_4^0 \\ 
W_4^0 & W_4^1 & W_4^2 & W_4^3 \\ 
W_4^0 & W_4^2 & W_4^4 & W_4^6 \\ 
W_4^0 & W_4^3 & W_4^6 & W_4^9 
\end{bmatrix} \begin{bmatrix} 
x[0] \\
x[1] \\
x[2] \\
x[3] \\
\end{bmatrix}
$$

其中 $W_N^{nk} = e^{-j\frac{2\pi}{N}nk}$。

**阶段 2：首次分解（奇偶分离）**

将输入序列按索引奇偶重排：偶数部分 $[x[0], x[2]]$，奇数部分 $[x[1], x[3]]$，DFT 可拆为两个矩阵之和：

$$
\mathbf{X} = 
\underbrace{
\begin{bmatrix}
W_4^0 & W_4^0 \\
W_4^0 & W_4^2 \\
W_4^0 & W_4^4 \\
W_4^0 & W_4^6
\end{bmatrix}
\begin{bmatrix}
x(0) \\
x(2) \\
\end{bmatrix}
}_{\text{偶样本部分}}
+ 
\underbrace{
\begin{bmatrix}
W_4^0 & W_4^0 \\
W_4^1 & W_4^3 \\
W_4^2 & W_4^6 \\
W_4^3 & W_4^9
\end{bmatrix}
\begin{bmatrix}
x(1) \\
x(3) \\
\end{bmatrix}
}_{\text{奇样本部分}}
$$

**阶段 3：旋转因子分离与块矩阵化**


利用旋转因子的**周期性** ($W_N^N=W_N^0$)、**折叠性** ($W_N^{N/2+k} = -W_N^k$)、**降阶**（ $W_N^{2k} = W_{N/2}^k$），为了进一步提取通用结构，将矩阵拆解为块矩阵与旋转因子矩阵的乘积：

$$
\mathbf{X} = \begin{bmatrix}
W_2^0 & W_2^0 \\
W_2^0 & W_2^1 \\
W_2^0 & W_2^0 \\
W_2^0 & W_2^1
\end{bmatrix}
\begin{bmatrix}
x(0) \\
x(2) \\
\end{bmatrix}
+
\underbrace{
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & W_4^1 & 0 & 0 \\
0 & 0 & W_4^2 & 0 \\
0 & 0 & 0 & W_4^3
\end{bmatrix}
}_{\text{旋转因子对角矩阵}}
\underbrace{
\begin{bmatrix}
W_2^0 & W_2^0 \\
W_2^0 & W_2^1 \\
W_2^0 & W_2^0 \\
W_2^0 & W_2^1
\end{bmatrix}
}_{\text{与偶样本相同}}
\begin{bmatrix}
x(1) \\
x(3) \\
\end{bmatrix}
$$

$$
\mathbf{X} = \begin{bmatrix} 
\mathbf{I}_2 & \mathbf{D}_2 \\ 
\mathbf{I}_2 & -\mathbf{D}_2 
\end{bmatrix} 
\begin{bmatrix} 
\mathbf{W}_2 & 0 \\ 
0 & \mathbf{W}_2 
\end{bmatrix} 
\begin{bmatrix} 
x[0] \\
x[2] \\
x[1] \\
x[3] \\
\end{bmatrix}
$$


其中：

- $\mathbf{I}_2$ 为单位矩阵
- 旋转因子对角矩阵 $\mathbf{D}_2 = $

$$
\begin{bmatrix} W_4^0 & 0 \\
0 & W_4^1 \\ 
\end{bmatrix}
$$

- 2 点 DFT 矩阵 $\mathbf{W}_2 =$
  
$$
\begin{bmatrix} W_2^0 & W_2^0 \\
W_2^0 & W_2^1 \\
\end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 
1 & -1 \\
\end{bmatrix}
$$

**阶段 4：简化为 2 点 DFT 形式**

展开后得到蝶形运算的两个分组：

$$
\begin{aligned} 
\begin{bmatrix} X[0] \\
X[1] \\ \end{bmatrix} &= \mathbf{W}_2 \begin{bmatrix} x[0] \\
x[2] \\ \end{bmatrix} + \mathbf{D}_2 \mathbf{W}_2 \begin{bmatrix} x[1] \\
x[3] \\ \end{bmatrix} \\ 
\begin{bmatrix} X[2] \\
X[3] \\ \end{bmatrix} &= \mathbf{W}_2 \begin{bmatrix} x[0] \\
x[2] \\ \end{bmatrix} - \mathbf{D}_2 \mathbf{W}_2 \begin{bmatrix} x[1] \\
x[3] \\ \end{bmatrix} 
\end{aligned}
$$

即经典的两点 DFT 加上旋转因子修正。

------

## 2. 8 点 FFT 的完整矩阵嵌套分解

将上述过程推广到 $N=8$，FFT 可以表示为三个稀疏矩阵 $\mathbf{A}_i$ 的乘积：

$$
\mathbf{X} = \mathbf{A}_3 \cdot \mathbf{A}_2 \cdot \mathbf{A}_1 \cdot \mathbf{P}_8 \mathbf{x}
$$

**第一级（最细粒度）：四个 2 点 DFT**

$$
\mathbf{A}_1 = \begin{bmatrix} 
\mathbf{W}_2 & & & \\ 
& \mathbf{W}_2 & & \\ 
& & \mathbf{W}_2 & \\ 
& & & \mathbf{W}_2 
\end{bmatrix}, \quad
\mathbf{W}_2 = \begin{bmatrix} 
1 & 1 \\
1 & -1 \\
\end{bmatrix}
$$

**第二级：4 点融合层**

$$
\mathbf{A}_2 = \begin{bmatrix} 
\mathbf{I}_2 & \mathbf{D}_2 & & \\ 
\mathbf{I}_2 & -\mathbf{D}_2 & & \\ 
& & \mathbf{I}_2 & \mathbf{D}_2 \\ 
& & \mathbf{I}_2 & -\mathbf{D}_2 
\end{bmatrix}, \quad
\mathbf{D}_2 = \begin{bmatrix} W_4^0 & 0 \\
0 & W_4^1 \\
\end{bmatrix}
$$

**第三级：8 点终极融合层**

$$
\mathbf{A}_3 = \begin{bmatrix} 
\mathbf{I}_4 & \mathbf{D}_4 \\ 
\mathbf{I}_4 & -\mathbf{D}_4 
\end{bmatrix}, \quad
\mathbf{D}_4 = 
\begin{bmatrix}
W_8^0 & 0 & 0 & 0 \\
0 & W_8^1 & 0 & 0 \\
0 & 0 & W_8^2 & 0 \\
0 & 0 & 0 & W_8^3
\end{bmatrix}
$$

**置换矩阵 $\mathbf{P}_8$（位序倒置）**

$\mathbf{P}_8$ 将输入顺序 $[0,1,2,3,4,5,6,7]$ 重排为 $[0,4,2,6,1,5,3,7]$，对应二进制位逆序。

------

## 3. 蝶形图：矩阵运算的几何映射

<p align="center">
<img src="/images/2_6_矩阵分解视角下的快速傅里叶变换FFT\FFT8点蝶形图.png" width="600" alt="Aliasing Demo Image 1">
</p>

这张 8 点蝶形图，完美诠释了矩阵分解后的数据流向：

- **输入洗牌**：最左侧输入 $x(0), x(4), x(2), x(6)\dots$ 对应置换矩阵 $\mathbf{P}_8$（位序倒置）。
- **计算级数**：每一列“蝴蝶结”代表一个稀疏矩阵相乘。
- **节点支路**：
  - **直线交叉**：对应矩阵中的 $\mathbf{I}$。
  - **乘数 $W_N^k$**：对应对角阵 $\mathbf{D}$ 中的旋转因子。
  - **-1 节点**：对应下半部分矩阵中的负号 $-\mathbf{D}$。

## 4. 计算量对比

通过上述矩阵分解，FFT 将稠密的 DFT 矩阵拆分为多个稀疏矩阵的乘积，大幅减少运算量。

| 变换方式     | 矩阵形式                   | 复数乘法估算                          |
| :----------- | :------------------------- | :------------------------------------ |
| **原始 DFT** | 1 个 $N \times N$ 稠密矩阵 | $N^2$（N=8 时为 64）                  |
| **FFT 分解** | $\log_2 N$ 个稀疏矩阵      | $\frac{N}{2} \log_2 N$（N=8 时为 12） |

## 5. 总结

1. **稀疏性**：每个 $\mathbf{A}_i$ 矩阵的每一行仅有 **2 个非零元素**，这意味着在每一级蝶形运算中，每个节点只接收两个输入——这正是蝶形图“交叉连接”的数学本质。
2. **旋转因子的分布**：
   - 第一层使用 $\mathbf{W}_2$（即 $\pm 1$，无复数乘法）
   - 第二层引入 $W_4$ 旋转因子
   - 第三层引入 $W_8$ 旋转因子
   - 随着级数增加，旋转因子覆盖单位圆上更细微的角度，实现频率分辨率的逐步细化。

通过这种层级化的矩阵分解，FFT 将原始 DFT 的 $O(N^2)$ 复杂度降低至 $O(N \log N)$，成为数字信号处理中最重要的算法之一。

**💡 延伸阅读：FFT 的“前世今生”**

为了更直观地感受这个算法的威力，推荐观看：[**Veritasium: 史上最重要的算法**](https://www.bilibili.com/video/BV1CY411R7bA/)

**为什么FFT算法能改变历史？**

* **诞生背景**：冷战时期，美国为了监测苏联是否在地下偷偷搞核试验，急需分析地震波频率。
* **计算奇迹**：按当时的算力，用普通 DFT 计算 100 万个点要 **3 年**，而用 FFT 只需要 **35 分钟**。这让实时监测成为了可能。
* **遗憾的巧合**：高斯早在 1805 年就发明了 FFT，但没发表。如果早点公开，人类的通信技术可能提前 100 年爆发。

