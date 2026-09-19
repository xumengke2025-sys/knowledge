> v0.2历史记录。当前版本请参阅 QUALITY-V0.3.md 与 firmbuddy/IMPORT-V0.3.md。

# 验证说明

运行：

```bash
python scripts/validate.py
```

硬门禁：
- 每个行业必备8类核心文件；
- JSON/JSONL 可解析；
- facts/source 引用完整；
- verified 公司必须有 evidence；
- FirmBuddy 专家 category/businessDomain 对齐；
- 具身智能 Universe ≥40，verified ≥10，代表性专利 ≥8；
- 不允许把候选公司自动写成事实。

`QUALITY-REPORT.md` 记录人工边界检查。
