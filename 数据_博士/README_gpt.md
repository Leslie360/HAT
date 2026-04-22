# 数据_博士 说明

这个目录存放博士提供或从博士 PPT / Origin 导出的原始数据与辅助拟合数据，供 `compute_vit` 的 measured-profile 拟合与审计使用。

## 目录结构

### 第三页
对应 PPT 第 3 页 `光突触`。

- `a/大图.txt`
  - 大图主曲线导出
  - 当前只作为背景辅助，不直接注入 nonvolatile profile
- `a/小图.txt`
  - `Origin ExpDec1 fit of G` 的拟合报告导出
  - 这是拟合/残差诊断表，不是原始 `PPF index vs ΔT` 散点表
- `a/小图_raw_ppf_points.txt`
  - 手动确认后的原始 PPF inset 点
  - 两列含义：`delta_t_raw`, `ppf_percent`
- `b/5-20paule.txt`
  - pulse-count / EPSC 相关曲线
- `c/300-800.txt`
  - pulse-width / EPSC 相关曲线
- `g/图.txt`
  - 8 条 RC state decay / response 曲线
- `h/100sID.txt`
  - `t = 100 s` 读取的 8-state 电流值

### 第四页
对应 PPT 第 4 页 `非易失性-多级存储展示-300℃退火`。

- `d/256次线性作图.txt`
  - multistate programming curve
  - 当前用于 `pulse_count_max` 与 programming residual noise
- `d/fitlinearcurvel.txt`
  - 上述编程曲线的拟合辅助文件
- `e/s0-s5.txt`
  - duplicated retention / repeatability curves
  - 当前用于 retention 与 repeatability (`sigma_c2c`) 拟合
- `i/pot.txt`
  - photoresponse sweep
  - 当前用于 `gamma_phys`, `I_dark`, `responsivity_alpha` 拟合
- `k/pot.txt`
  - pulse-width dependence
  - 当前保留为辅助证据，未直接注入 JSON
- `l/pot.txt`
  - panel `(l)/(m)` 相关时间序列
  - 当前保留，未强行注入 JSON，因为 `(l)` / `(m)` 语义仍需谨慎映射

### 第20页
对应 PPT 第 20 页 `多级-Rc计算用数据16/64状态`。

- `16.txt`
  - RC-16 ladder / state trace
  - 当前用于提取 `Doctor OECT Nonvolatile RC-16` 的 `inl_table`
- `64.txt`
  - RC-64 ladder / state trace
  - 当前用于提取 `Doctor OECT Nonvolatile RC-64` 的 `inl_table`

## 当前已生成的下游产物

- `report_md/_gpt/json_gpt/doctor_measured_profiles.json`
- `report_md/_gpt/json_gpt/doctor_measured_profile_summary.json`
- `report_md/_gpt/DOCTOR_MEASURED_PROFILE_AUDIT_20260416.md`
- `report_md/_gpt/DOCTOR_MEASURED_PROFILE_VALIDATION_20260416.md`

## 注意

- `第三页/a/小图.txt` 本身不是 raw PPF 散点；真正的 raw PPF 点已单独写入 `第三页/a/小图_raw_ppf_points.txt`
- 当前 JSON profile 主要服务于 nonvolatile weight-storage / vision inference 路径
- volatile / PPF / RC 数据已归档，但未全部映射到当前 `DeviceProfile` schema
