# 后端问题排查

## 常见问题

### 1. 大量"请求失败"日志

**现象**：启动后看到很多"请求 XXX 失败"的消息

**原因**：这是正常的！系统在扫描IP范围时，很多IP地址不是矿机，连接失败是预期行为。

**解决**：
- 默认情况下，这些错误日志已经被静默处理
- 如果需要查看详细日志，在 `backend/config.py` 中设置 `DEBUG_MODE = True`

### 2. 定时任务警告

**现象**：
```
Execution of job "discover_new_miners" skipped: maximum number of running instances reached
Run time of job "update_all_miners_status" was missed
```

**原因**：
- IP扫描范围太大（320个IP），扫描时间超过任务间隔
- 定时任务执行时间过长

**已优化**：
- ✅ 增加了任务间隔时间（扫描5分钟，状态更新1分钟）
- ✅ 添加了超时控制（每个IP最多2秒）
- ✅ 优化了批次大小（100个IP一批）
- ✅ 添加了任务合并机制（coalesce）

**如果仍有问题**：
1. 减少IP扫描范围（编辑 `backend/config.py` 中的 `IP_RANGES`）
2. 增加扫描间隔（编辑 `SCAN_INTERVAL`）
3. 只扫描已知的矿机IP，而不是整个范围

### 3. 关闭时的错误

**现象**：按 Ctrl+C 关闭时看到 `CancelledError` 或 `KeyboardInterrupt`

**原因**：这是正常的！当您关闭服务时，正在运行的定时任务会被取消。

**解决**：无需处理，这是正常的关闭行为。

### 4. 性能优化建议

如果IP范围很大（>200个IP），建议：

1. **只扫描已知的矿机IP**：
   ```python
   # 在 backend/config.py 中
   IP_RANGES = [
       ("10.102.0.1", "10.102.0.112"),  # 只扫描您知道有矿机的范围
   ]
   ```

2. **手动添加矿机**（推荐）：
   - 使用API手动添加：`POST /api/miners/discover`
   - 或直接编辑数据库添加已知的矿机IP

3. **增加扫描间隔**：
   ```python
   SCAN_INTERVAL = 600  # 10分钟扫描一次
   ```

## 配置说明

在 `backend/config.py` 中可以调整：

- `DEBUG_MODE`: 是否显示详细错误日志（默认False）
- `SCAN_INTERVAL`: IP扫描间隔（默认300秒）
- `STATUS_UPDATE_INTERVAL`: 状态更新间隔（默认60秒）
- `API_TIMEOUT`: API请求超时（默认3秒）
- `IP_RANGES`: IP扫描范围

## 日志级别

- **正常模式**（DEBUG_MODE=False）：只显示重要信息
- **调试模式**（DEBUG_MODE=True）：显示所有错误详情

## 性能指标

- IP扫描：约2-3秒/100个IP
- 状态更新：约1-2秒/矿机
- 推荐矿机数量：<200台（超过可能需要优化）
