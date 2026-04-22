# 学位论文中文 LaTeX 模板选型与格式要求

> 文档编号：KIMI-THESIS-CN-TEMPLATE-20260420  
> 适用范围：`compute_vit/paper/thesis_cn/` 学位论文编译  
> 撰写：Kimi Phase α Round P2

---

## 1. 常见中国高校学位论文 LaTeX 模板调研

### 1.1 候选模板概览

| 模板名称 | 主维护高校 | 许可证 | 特点与适用场景 |
|---------|-----------|--------|---------------|
| **thuthesis** | 清华大学 | LPPL 1.3c | 历史最悠久、社区最大、文档最完善；支持本科/硕士/博士及博士后报告；对数学、物理、计算机类公式排版极成熟。 |
| **ustcthesis** | 中国科学技术大学 | LPPL 1.3c | 代码结构清晰，严格遵循《中国科学技术大学研究生学位论文撰写规范》；对图表浮动体、双语目录支持优秀。 |
| **chinathesis** | 南京大学（为主） | LPPL 1.3c | 原名 nju-thesis，后扩展为通用框架；通过配置切换多所高校格式；适合尚未确定最终学校的初稿阶段。 |
| **sjtuthesis** | 上海交通大学 | Apache-2.0 | 与学校 Overleaf 官方镜像同步更新；对英文摘要、符号表、攻读学位期间取得成果清单支持好。 |
| **cas-ustc-thesis** | 中国科学院大学 | LPPL 1.3c | 针对中科院体系（含各研究所）规范；对超大量参考文献、多附录场景优化好。 |
| **pkuthss** | 北京大学 | LPPL 1.3c | 极简风格，宏包依赖少；适合对编译速度敏感、希望底层可控的用户。 |

### 1.2 模板对比维度

#### (1) 参考文献样式
- `thuthesis`、`ustcthesis`、`chinathesis` 均原生支持 `gbt7714-numerical`（GB/T 7714—2015 顺序编码制），与本研究 BibTeX 库兼容。
- `sjtuthesis` 默认使用 `natbib` + `gbt7714`，需手动关闭作者--年份制以避免混淆。
- `pkuthss` 默认使用 `biblatex` + `gb7714-2015`，与当前基于 BibTeX 的 `references.bib` 需要额外适配（建议改用 `biblatex` 后端或转换条目格式）。

#### (2) 中英文混排与字体
- 所有候选模板均基于 `ctex` 宏包，支持 Windows（MiKTeX/TeX Live）、macOS、Linux（Fandol 或系统字体）跨平台编译。
- `thuthesis` 对 Windows 字体（SimSun、SimHei、Times New Roman）支持最成熟；若使用 Linux，需配置 `fontset=fandol` 或手动指定思源字体。
- `ustcthesis` 在 Linux 下默认调用 `fontset=fandol`，开箱即用性最佳。

#### (3) 图表与浮动体
- `thuthesis` 提供 `\thusetup` 配置接口，可一键切换图表标题样式（如“图 4-1”或“图 4.1”）。
- `ustcthesis` 的图表标题默认使用 `"--"` 连接符（如 `"图 4--1"`），与部分高校规范一致。
- `chinathesis` 通过 `style` 键值对（如 `style = nju|thu|ustc`）自动适配不同学校的图表编号规则。

#### (4) 页眉页脚
- `thuthesis`：博士论文默认“奇数页章标题 + 偶数页论文题目”，硕士论文可简化为居中页码。
- `ustcthesis`：严格遵循校规范，页眉为 `"中国科学技术大学博士学位论文"`，页脚居中页码。
- `sjtuthesis`：支持 `"第 X 章 章标题"` 与 `"上海交通大学博士学位论文"` 交替页眉。

#### (5) 编译方式
- 全部支持 `xelatex`（推荐）与 `lualatex`。
- `thuthesis`、`ustcthesis` 提供 `latexmk` 配置文件（`.latexmkrc`），支持 `latexmk -xelatex` 一键编译。
- `chinathesis` 额外支持 `tectonic` 编译（与本项目英文版 `main.tex` 的 `!TeX program = tectonic` 保持一致）。

---

## 2. 推荐模板及理由

### 2.1 首选推荐：thuthesis

**推荐理由：**

1. **社区与文档成熟度最高**：GitHub Stars 3k+，Issue 响应及时，覆盖 Windows/macOS/Linux 全平台常见问题。对于需要频繁调整格式（如图表编号、页眉页脚）的交叉学科论文（本研究涉及计算机视觉、器件物理、电路系统），成熟的社区支持可显著降低排版调试时间。

2. **与本研究 BibTeX 库零适配成本**：`thuthesis` 默认加载 `gbt7714-numerical` 样式，可直接消费 `references.bib`，无需修改条目字段或转换 `biblatex` 语法。

3. **图表与公式排版经验证**：本研究含大量模拟精度表格（如第 4 章表 4-1~4-5）、ADC 精度扫描图、保留衰减曲线。`thuthesis` 对 `booktabs` 三线表、`subcaption` 子图、`siunitx` 单位标注的兼容性经过多届博士论文验证。

4. **章节编号灵活**：支持 `"第X章"` 中文编号（`第\chinese{chapter}\u7ae0`）与阿拉伯数字编号切换，适合学校规范不明确时的快速调整。

**潜在注意事项**：
- 若最终学校非清华，需通过 `\thusetup` 关闭校徽封面、调整页眉文字。
- Linux 环境下需确认已安装思源宋体/黑体或配置 `fontset=fandol`。

### 2.2 备选推荐：ustcthesis

若最终学校为中国科学技术大学或中国科学院体系，**ustcthesis** 为更优选择：
- 与学校《研究生学位论文撰写规范》逐条对齐，减少后续格式审查修改。
- 对“攻读学位期间取得成果”清单有原生环境（`achievement`），本研究涉及多篇在投/已发表论文，可直接复用。

### 2.3 跨校迁移保险方案：chinathesis

若当前尚未确定最终答辩学校，可使用 `chinathesis` 作为初稿框架：
- 通过 `\documentclass[style=thu]{chinathesis}` 或 `style=ustc` 等配置，在初稿阶段即可预览不同学校的格式差异。
- 定稿后若需切换至 `thuthesis` 或 `ustcthesis`，正文内容（`章`、`节`、公式、图表）无需修改，仅需调整导言区与封面文件。

---

## 3. 格式检查清单

以下清单基于 GB/T 7713.1—2006《学位论文编写规则》及常见高校补充规范编制，
适用于 `thuthesis` 或其他基于 `ctex` 的模板。

### 3.1 页面设置

| 检查项 | 规范要求 | `thuthesis` 配置键 |
|--------|---------|-------------------|
| 纸张 | A4（210 mm × 297 mm） | 默认 |
| 页边距 | 上 2.54 cm、下 2.54 cm、左 3.17 cm、右 3.17 cm（博士常见）；或上/下 2.54 cm、左 3.0 cm、右 2.5 cm（硕士常见） | `geometry` 包参数 |
| 行距 | 正文 1.5 倍或固定 20 pt | `\thusetup{line-spread = 1.5}` |
| 段落缩进 | 首行缩进 2 字符 | `\ctexset{autoindent = true}` |

### 3.2 页眉页脚

| 检查项 | 规范要求 | `thuthesis` 实现 |
|--------|---------|-----------------|
| 封面/声明页 | 无页眉页脚，不编页码 | 模板已处理 |
| 中英文摘要 | 页眉为“摘要”或“Abstract”，页脚居中罗马数字页码（i, ii, iii...） | 模板已处理 |
| 目录页 | 页眉为“目录”，页脚居中罗马数字 | 模板已处理 |
| 正文页 | 奇数页页眉为章标题，偶数页页眉为论文题目；页脚居中阿拉伯数字页码 | `\pagestyle{thu}` |
| 参考文献/附录 | 同正文页眉页脚规则 | 自动继承 |

### 3.3 章节编号

| 检查项 | 规范要求 | LaTeX 实现 |
|--------|---------|-----------|
| 章 | `"第1章"`、`"第2章"`... 或 `"1 引言"`、`"2 相关工作"`... | `\ctexset{chapter/name = {第,章}}` 或清空 `name` |
| 节 | `"1.1"`、`"1.2"`... | `\section` |
| 小节 | `"1.1.1"`、`"1.1.2"`... | `\subsection` |
| 目录深度 | 显示至 `\subsection`（三级） | `\setcounter{tocdepth}{2}` |
| 章标题字体 | 黑体（SimHei）三号或 16 pt | `\ctexset{chapter/format = \zihao{3}\heiti}` |
| 节标题字体 | 黑体四号或 14 pt | `\ctexset{section/format = \zihao{4}\heiti}` |

### 3.4 图表标题

| 检查项 | 规范要求 | LaTeX 实现 |
|--------|---------|-----------|
| 图标题 | `"图 3-1"` 或 `"图 3--1"` 或 `"图 3.1"`，位于图下方，宋体五号 | `\captionsetup[figure]{labelsep=space}` 或 `labelsep=quad` |
| 表标题 | `"表 3-1"`... 位于表上方，宋体五号 | `\captionsetup[table]{labelsep=space, position=above}` |
| 编号方式 | 章内连续编号（如第 3 章的图编号为 3-1, 3-2...） | `\renewcommand{\thefigure}{\thechapter-\arabic{figure}}` |
| 长表 | 跨页表格使用 `longtable` 或 `supertabular`，每页重复表头 | `\endhead` |

### 3.5 参考文献样式

| 检查项 | 规范要求 | LaTeX 实现 |
|--------|---------|-----------|
| 著录格式 | GB/T 7714—2015 顺序编码制 | `\bibliographystyle{gbt7714-numerical}` |
| 正文中引用 | 上标数字，如 `"... 存内计算架构 [1] 通过在..."` | `\usepackage[super,sort&compress]{natbib}` + `\citep{key}` |
| 参考文献列表 | 按引用顺序编号，悬挂缩进 2 字符 | `gbt7714-numerical` 默认 |
| 电子资源 | DOI 优先，arXiv 需标注 `arXiv preprint` | `references.bib` 中已保留 `doi` 与 `eprint` 字段 |
| 中文文献 | 作者名保留中文，题名后加注 `[J]`、`[C]`、`[D]` 等文献类型标志 | 若后续添加中文文献，需确保 BibTeX 条目包含 `language = {zh}` 字段，以触发 `gbt7714` 的中文格式分支 |

### 3.6 数学与符号

| 检查项 | 规范要求 | LaTeX 实现 |
|--------|---------|-----------|
| 公式编号 | 章内连续编号，如 `"(3-1)"`、`"(3-2)"` | `\renewcommand{\theequation}{\thechapter-\arabic{equation}}` |
| 变量字体 | 物理量用斜体，单位用正体 | `\si{}`（`siunitx`）或手动 `\mathrm{}` |
| 矩阵/向量 | 矩阵大写粗斜体 `\mathbf{}`，向量小写粗斜体 | `\usepackage{bm}` + `\bm{A}`、`\bm{x}` |
| 定义/定理环境 | 使用 `"定义 3.1"`、`"定理 3.1"` 编号 | `\newtheorem{definition}{定义}[chapter]` |

### 3.7 封面与前置部分

| 检查项 | 规范要求 | 备注 |
|--------|---------|------|
| 学校代码 | 按学校统一代码填写 | 待最终学校确定后填入 |
| 分类号 | 中图法分类号（如 TP391.4） | 本研究属 `"计算机应用技术"`，建议 TP391.4 或 TP212 |
| UDC 号 | 国际十进分类号 | 待查 |
| 密级 | 公开 / 内部 / 秘密 / 机密 | 默认 `"公开"` |
| 论文题目 | 中文不超过 25 字，英文实词首字母大写 | 当前占位 `[THESIS TITLE]` |
| 作者姓名 | 与学籍信息一致 | `Li Songqiao` |
| 导师姓名 | `[导师姓名]` 占位 | 待用户提供 |
| 答辩日期 | `[Date]` 占位 | 待用户提供 |

### 3.8 编译检查

| 检查项 | 通过标准 |
|--------|---------|
| 无 Overfull/Underfull 警告 | `latexmk -xelatex` 编译后无 `Overfull \hbox` 或控制在可接受范围（badness < 10000） |
| 交叉引用正确 | 所有 `\ref{}`、`\citep{}`、`\label{}` 经两次编译后解析正确，无 `??` 或 `[?]` |
| 目录页码一致 | 目录中的页码与实际正文页码一致 |
| 图表编号连续 | 无重复或跳号 |
| PDF 书签 | 使用 `hyperref` 生成，中文书签无乱码（`xelatex` 默认支持） |
| 字体嵌入 | `pdffonts main.pdf` 显示所有字体已嵌入（`yes`），无 `"no"` 项 |

---

## 4. 快速启动命令（thuthesis 示例）

```bash
# 1. 克隆模板
git clone https://github.com/tuna/thuthesis.git
cd thuthesis

# 2. 安装依赖（TeX Live 2023+）
tlmgr install gbt7714 natbib booktabs siunitx subcaption cleveref

# 3. 将本研究文件放入模板目录
cp /path/to/thesis_cn/chapter_*.tex ./data/
cp /path/to/thesis_cn/references.bib ./
cp /path/to/thesis_cn/front_matter.tex ./data/

# 4. 编译
latexmk -xelatex thuthesis-example.tex

# 5. 检查输出
pdffonts thuthesis-example.pdf
```

---

## 5. 与本项目现有文件的衔接说明

本项目英文版论文使用 `report` 文档类 + `natbib` + `unsrtnat` 样式，中文版切换为 `thuthesis`（或 `ctexbook`）时，需注意以下衔接点：

| 衔接项 | 英文版现状 | 中文版调整 |
|--------|-----------|-----------|
| 文档类 | `\documentclass[12pt]{report}` | `\documentclass[degree=doctor]{thuthesis}` 或 `\documentclass{ctexbook}` |
| 参考文献样式 | `\bibliographystyle{unsrtnat}` | `\bibliographystyle{gbt7714-numerical}` |
| natbib 选项 | `[super,sort&compress]` | 保持 `super` 以生成上标引用 |
| 图表路径 | `\graphicspath{{../latex_gpt/figures/}}` | 保持不变，或复制 figures 到 `figures/` |
| 自定义宏 | `\SuppFigNoiseSweep` 等 | 保留，置于导言区 |
| 章节文件 | `\include{chapter_4_failure_modes}` | `\include{data/chapter_4_benchmarks}`（对应中文论文结构） |

---

## 6. 结论

- **推荐模板**：`thuthesis`（首选）、`ustcthesis`（若最终学校为中科大/中科院体系）。
- **核心原则**：在初稿阶段优先保证内容完整与数据准确，格式通过模板配置统一管控；避免在正文中硬编码字体、字号、页边距等排版参数。
- **下一步行动**：待用户提供最终学校名称与学位类型（硕士/博士）后，可生成具体的 `main.tex` 导言区与封面配置。
