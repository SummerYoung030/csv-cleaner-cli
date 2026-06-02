# csv-cleaner-cli

Benchmark Task：Python CLI 清洗 CSV 数据。

## 一键在线测试

将本项目推送到 GitHub 后，打开 **Actions** 页面，点击 **Run workflow** 即可触发评测：

[一键测试（GitHub Actions）](https://github.com/SummerYoung030/csv-cleaner-cli/actions/workflows/benchmark-test.yml)

```
https://github.com/SummerYoung030/csv-cleaner-cli/actions/workflows/benchmark-test.yml
```

绿色 ✓ 表示 `tests/test.sh`（Docker build + run）全部通过。

## 本地测试

### 官方入口（与评测机一致）

```bash
bash tests/test.sh
echo $?   # 0 = 通过
```

### 无 Docker 冒烟测试

```bash
bash tests/test_local.sh
```

## 目录结构

```
csv-cleaner-cli/
├── task.toml
├── instruction.md
├── environment/
│   ├── Dockerfile
│   └── dirty_data.csv
├── solution/
│   ├── cleaner.py
│   └── solve.sh
└── tests/
    ├── test_logic.py
    ├── test.sh
    └── run_in_container.sh
```
