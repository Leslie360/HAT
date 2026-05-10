# 📢 广播：npj Computational Materials 策略确认

> **日期**: 2026-04-13  
> **决策**: 确认npj Computational Materials为投稿目标  
> **状态**: Package initialized, repositioning in progress

---

## ✅ 已完成设置

### 1. npj提交包目录结构
```
npj_submission_package/
├── manuscript/              # 主LaTeX源文件
├── supplementary/           # Supplementary Information
├── figures/                 # 高清图文件
├── source_data/            # 源数据表格
├── cover_letter/           # 封面信
└── response_to_reviewers/  # 审稿回应模板
```

### 2. 交付文档

| 文件 | 内容 | 状态 |
|:-----|:-----|:----:|
| `README.md` | 包说明、时间线、成功指标 | ✅ |
| `REPOSITIONING_GUIDE.md` | 10步重定位指南 | ✅ |
| `cover_letter/npj_cover_letter.tex` | npj专用封面信 | ✅ |

---

## 🎯 核心重定位要点

### 叙事转变

| 维度 | NC定位 | npj定位 |
|:-----|:-------|:--------|
| **Primary Contribution** | Ensemble HAT算法 | Materials-to-system方法学 |
| **Audience** | ML systems + materials | Materials science |
| **Validation Expectation** | High (hardware closure) | Moderate (methodology rigor) |
| **Key Selling Point** | Algorithm novelty | Simulation methodology |
| **Acceptance Confidence** | ~60% | ~80% |

### 必须修改

1. **Title**: Add "Methodology" or "Simulation Framework"
2. **Abstract**: Foreground materials characterization gap
3. **Contributions**: Reorder (profile interface first, HAT fourth)
4. **Related Work**: Add "Computational Materials Tools" section
5. **Discussion**: Add "Implications for Materials Characterization"

---

## 📊 Venue比较确认

| Factor | NC | npj Comp Mat | 选择理由 |
|:-------|:---|:-------------|:---------|
| Acceptance | ~60% (Major Rev) | ~80% (Minor Rev) | ✅ 高接受率 |
| Hardware bar | High | Moderate | ✅ 适合仿真 |
| Methodology | Welcomed | Explicitly | ✅ 更好匹配 |
| Review cycle | 3-4 months | 2-3 months | ✅ 更快 |
| Impact Factor | ~16 | ~9-10 | 权衡接受 |

**战略判断**: npj是正确选择——保持Nature portfolio质量，提高接受信心。

---

## 📝 下一步任务

### Week 1 (2026-04-13 to 04-20)

| 任务 | 负责人 | 工作量 | 依赖 |
|:-----|:-------|:-------|:-----|
| 重定位manuscript | Codex | 2天 | 本广播 |
| 添加Computational Materials相关章节 | Codex | 1天 | 重定位指南 |
| 扩展device physics讨论 | Codex | 1天 | - |
| 准备Parameter Risk Matrix | Kimi | 已准备 | 插入Supp |

### Week 2 (2026-04-20 to 04-27)

| 任务 | 负责人 | 工作量 |
|:-----|:-------|:-------|
| 编译最终manuscript | Codex | 0.5天 |
| 准备source data表格 | Codex | 0.5天 |
| 最终cover letter | Kimi | 已准备 |
| 投稿系统上传 | 用户 | 0.5天 |

---

## 🎁 预加载资产

### 防守弹药 (Kimi已完成)
- ✅ Parameter Risk Matrix
- ✅ 8条proxy-parameter防守
- ✅ 13条editor/reviewer回应

### 实验补充 (可选)
- 🔄 Ensemble HAT对照实验 (GM-E1/E2)
- ⏸️ 用户自有数据 (Revision阶段)

---

## 💡 关键成功因素

1. **不要隐藏仿真性质** — npj接受纯方法学，但要求透明度
2. **强调materials-to-system桥** — 这是核心贡献
3. **Parameter Risk Matrix** — 将代理参数弱点转为优势
4. **为未来measured-data铺路** — 接口设计的前瞻性

---

## 📡 广播对象

- @Codex: 执行REPOSITIONING_GUIDE.md中的10步修改
- @Gemini: 如有GPU资源，继续GM-E1/E2对照实验 (optional)
- @用户: 确认timeline，准备投稿系统账户

---

**npj Computational Materials投稿包已就绪。等待Codex执行重定位修改。**
