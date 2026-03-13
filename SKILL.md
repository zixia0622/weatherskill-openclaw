---
name: weather-push
description: 天气预报获取与推送。当用户要求查天气、发送天气预报、天气播报、定时天气推送、每日天气提醒时触发。支持国内15个主要城市，可通过经纬度扩展到任意地点。数据源为 Open-Meteo API（免费，无需 API Key）。
---

# 天气预报推送 Skill

## 快速使用

### 获取天气数据

```bash
# 单城市（默认北京）
python3 <skill_dir>/scripts/fetch_weather.py

# 指定城市
python3 <skill_dir>/scripts/fetch_weather.py --city 上海

# 多城市
python3 <skill_dir>/scripts/fetch_weather.py --cities 北京,上海,广州

# 自定义经纬度
python3 <skill_dir>/scripts/fetch_weather.py --lat 31.23 --lon 121.47 --city 上海

# JSON 输出（适合程序化处理）
python3 <skill_dir>/scripts/fetch_weather.py --city 北京 --json
```

### 支持的城市

北京、上海、广州、深圳、成都、杭州、武汉、南京、西安、重庆、长沙、天津、苏州、郑州、厦门。

不在列表中的城市：使用 `--lat` `--lon` 参数传入经纬度。

## 推送流程

1. 运行 `scripts/fetch_weather.py` 获取天气数据
2. 根据用户要求选择输出格式（文字播报或 JSON）
3. 通过用户指定的渠道发送（大象、Telegram、微信等）

### 文字播报格式

脚本默认输出格式：
```
🌤️ {城市}今日天气
当前: {天气描述} {温度}°C
最高 {最高温}°C | 最低 {最低温}°C
风速: {风速} km/h
{降水/紫外线/生活建议}

📅 未来预报:
  {日期} | {天气} | {温度范围}
```

可根据用户偏好自定义格式，如更简洁或更详细。

### 定时推送

配合 OpenClaw cron 定时任务实现每日自动推送：
- 在对话中设置："每天早上8点给我发北京天气"
- Agent 创建 cron 任务，定时运行此 Skill 并发送结果

## 数据说明

- **数据源**: Open-Meteo API（开源免费，无需注册）
- **更新频率**: 实时查询，每次调用获取最新数据
- **预报范围**: 当天 + 未来2天
- **包含指标**: 温度、风速、降水量、紫外线指数、天气状况
- **生活建议**: 自动根据温度和降水生成（低温保暖/高温防暑/带伞提醒/防晒提醒）

## 扩展

添加新城市：编辑 `scripts/fetch_weather.py` 中的 `CITY_COORDS` 字典，添加城市名和经纬度。
