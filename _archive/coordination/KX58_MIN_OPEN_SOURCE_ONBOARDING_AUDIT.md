# KX58: Minimal Open-Source + Measured-Data Onboarding Audit

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Goal**: 最小清单，让项目能往真实仿真/开源继续走

---

## 核心原则

**最小可行**，非庞大愿望书。区分"必须现在做" vs "可以等Paper-2"。

---

## Part 1: Measured-Data Onboarding (P0 - 现在必须)

### 1.1 Profile Auto-Fitter 验证

| 项目 | 状态 | 行动 |
|:-----|:-----|:-----|
| `profile_auto_fitter_gpt.py` 存在 | ✅ | 已有，需测试 |
| 端到端 raw curve → JSON workflow | ⚠️ | 需用博士数据验证一次 |
| 错误处理 (bad data) | ❌ | 需添加；最小：graceful error + log |

**最小完成标准**: 能用真实器件的5组数据成功生成profile，不崩溃。

### 1.2 数据格式文档

| 项目 | 状态 | 行动 |
|:-----|:-----|:-----|
| 接受的输入格式说明 | ⚠️ | 需写：CSV/Excel列名要求 |
| 示例输入文件 | ❌ | 需创建：dummy_example.csv |
| 参数提取公式说明 | ⚠️ | 已有KX51，需整理进docs |

**最小完成标准**: 博士能拿着文档独立准备数据，无需我们协助。

### 1.3 结果验证协议

| 项目 | 状态 | 行动 |
|:-----|:-----|:-----|
| Measured-profile vs simulation 对比 | ⚠️ | 需跑通一次完整流程 |
| R² 或误差指标 | ❌ | 需添加：G-V曲线拟合优度 |

**最小完成标准**: 能说出"实测数据在仿真中的表现如何"。

---

## Part 2: Open-Source Release (P1 - Paper-1后)

### 2.1 代码清理

| 项目 | 状态 | 行动 | 优先级 |
|:-----|:-----|:-----|:------:|
| 移除硬编码路径 | ⚠️ | 所有 `_gpt` 路径改为 configurable | P0 |
| 添加requirements.txt | ⚠️ | 列出核心依赖 | P0 |
| 配置化参数 | ❌ | YAML/JSON config 替代内联参数 | P1 |
| 代码注释 | ⚠️ | 关键函数 docstring | P1 |

### 2.2 最小文档

| 项目 | 状态 | 行动 | 优先级 |
|:-----|:-----|:-----|:------:|
| README.md (安装+快速开始) | ⚠️ | 已有，需更新 | P0 |
| 简单示例 (train one model) | ⚠️ | 已有，需验证跑通 | P0 |
| API文档 | ❌ | 可以等；非阻塞 | P2 |
| Jupyter教程 | ❌ | Paper-2时添加 | P2 |

### 2.3 发布基础设施

| 项目 | 状态 | 行动 | 优先级 |
|:-----|:-----|:-----|:------:|
| GitHub repo 公开 | ⚠️ | 已有，设为public | P0 |
| LICENSE | ⚠️ | 添加 (MIT/Apache) | P0 |
| pip installable | ❌ | 可以等；setup.py | P1 |
| 预训练模型 zoo | ❌ | Paper-2时 | P2 |

---

## Part 3: 可以等 Paper-2 的 (P2)

| 项目 | 理由 |
|:-----|:-----|
| 完整API文档 | Paper-1接受后再投入 |
| 交互式教程 | 需要稳定API后 |
| 多器件批量处理 | 需要更多实测数据验证 |
| Web可视化界面 | 超出当前范围 |
| 社区贡献指南 | 有用户后再写 |

---

## 最小行动清单 (接下来2周)

### Week 1
- [ ] 用KX55模板向博士发送数据请求
- [ ] 收到数据后，跑通 `profile_auto_fitter_gpt.py` 一次
- [ ] 记录成功/失败，修复崩溃问题
- [ ] 写 `INPUT_FORMAT.md` (输入格式说明)

### Week 2
- [ ] 清理硬编码路径
- [ ] 更新README.md (安装说明)
- [ ] 验证示例脚本跑通
- [ ] 添加LICENSE文件
- [ ] 设GitHub repo为public

---

## 依赖关系

```
博士数据到达
    ↓
Profile Auto-Fitter 验证
    ↓
Measured-device case study (Paper-1 Revision或Paper-2)
    ↓
Open-source 发布 (有实测验证后更可信)
```

---

## 成功标准

| 里程碑 | 标准 |
|:-------|:-----|
| **最小开源** | 陌生人能clone→install→run一个示例 (CIFAR-10) |
| **实测数据就绪** | 能接收博士原始数据→生成profile→跑仿真 |
| **完整开源** | pip install + 教程 + 社区 (Paper-2后) |

---

## 当前 gaps 速览

| 类别 | 已完成 | 需现在做 | 可等待 |
|:-----|:-------|:---------|:-------|
| Measured-data onboarding | KX51模板, fitter脚本 | 验证一次, 写格式文档 | 批量处理工具 |
| Open-source infra | GitHub repo, 基础README | LICENSE, 清理路径, 验证示例 | pip, 文档, 教程 |
| Community | - | - | 全部等Paper-2 |

---

**状态**: 最小清单明确，2周内可完成P0/P1基础。
