# Figure 1 & 2 视觉修复建议

> **问题**: 字和线条卡在一起，整体绘制丑陋  
> **基于**: 用户描述无法直接查看图像

---

## 常见问题诊断

### 问题1: 字体过大/标签重叠
**症状**: 字和线条卡一块
**原因**: 
- 图中标签字体相对于图尺寸过大
- 多个标签靠得太近
- 使用了与正文相同大小的字体

**修复方案**:
```latex
% 在导言区添加
\usepackage{graphicx}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18,
    tick label style={font=\tiny},
    label style={font=\small},
    legend style={font=\tiny},
    every axis plot/.append style={thick}
}

% 或者对单个图
\begin{figure}[ht]
    \centering
    \includegraphics[width=0.85\textwidth]{fig1}  % 减小到0.85给边缘留空
    \caption{...}
\end{figure}
```

---

### 问题2: 线条过粗/颜色对比差
**症状**: 看起来"丑"，线条挤在一起
**修复**:
```python
# 如果是Python生成
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 8        # 减小字体
plt.rcParams['axes.labelsize'] = 9   # 轴标签
plt.rcParams['axes.titlesize'] = 10  # 标题
plt.rcParams['xtick.labelsize'] = 7  # x轴刻度
plt.rcParams['ytick.labelsize'] = 7  # y轴刻度
plt.rcParams['lines.linewidth'] = 1.5  # 线粗细
plt.rcParams['figure.dpi'] = 300     # 高分辨率

# 保存时留白
plt.tight_layout(pad=0.5)
plt.savefig('fig1.png', bbox_inches='tight', dpi=300)
```

---

### 问题3: 图中文字与线条重叠
**症状**: 标签压在线上
**修复策略**:

1. **调整标签位置**:
```python
# 使用annotate精确定位
plt.annotate('label', xy=(x, y), xytext=(x+offset, y+offset),
             arrowprops=dict(arrowstyle='->', color='gray'),
             fontsize=8, ha='center')
```

2. **使用图例而非直接标注**:
```python
# 不要直接在图上写字
plt.plot(x, y, label='Component A')  # 用图例
plt.legend(loc='upper right', fontsize=8)
```

3. **增加白色背景框**:
```python
from matplotlib.patches import FancyBboxPatch
# 给文字加白色背景
plt.text(x, y, 'Label', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
```

---

### 问题4: 图尺寸比例不当
**症状**: 图被压扁或拉伸
**修复**:
```python
# 设置合适的图尺寸
plt.figure(figsize=(8, 4))  # 宽度, 高度 (英寸)

# 或者使用黄金比例
plt.figure(figigsize=(10, 6.18))
```

---

## 针对具体图的建议

### Figure 1: System Architecture
**可能问题**:
- 框图太挤，模块标签重叠
- 箭头太粗与文字重叠

**建议**:
```python
# 使用更简洁的框图风格
# 减少不必要的细节
# 增大模块间距
# 使用统一字体大小
```

### Figure 2: Weight Mapping
**可能问题**:
- 数学符号太大
- 箭头标注重叠

**建议**:
```python
# 使用更小的数学字体
# 分步骤展示而非一次性展示
# 使用颜色区分而非文字标注
```

---

## 立即可执行的修复

### 方案1: 临时缩小图 (最快)
```latex
% 在LaTeX中减小图尺寸，让字体相对变小
\includegraphics[width=0.75\textwidth]{fig1_system_architecture}
% 原来是0.92，现在0.75
```

### 方案2: 强制字体大小
```latex
\begin{figure}[ht]
    \centering
    \small  % 添加这一行强制小字体
    \includegraphics[width=0.92\textwidth]{fig1_system_architecture}
    \caption{...}
\end{figure}
```

### 方案3: 使用pdf/clean版本
如果原图是PNG，建议:
1. 重新生成矢量图(PDF/SVG)
2. 使用更高分辨率(300+ DPI)
3. 清理边缘空白

---

## 专业建议

**最可能的问题组合**:
1. 图中标签字体 = 正文字体 (应该更小)
2. 元素过于密集 (应该增加间距)
3. 分辨率不够 (应该300+ DPI)

**推荐修复顺序**:
1. 先在LaTeX中缩小图尺寸 (测试)
2. 如果仍不行，重新生成图 (减小字体，增加间距)
3. 确保输出是矢量图或高分辨率PNG

---

**需要具体查看图像文件才能给出更精确的修复方案。**
