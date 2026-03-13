# 🌤️ weather-push

OpenClaw Skill —— 天气预报获取与推送。

## 功能

- 查询国内 15 个主要城市实时天气 + 未来 2 天预报
- 支持自定义经纬度查询任意地点
- 自动生成生活建议（保暖/防暑/带伞/防晒）
- 文字播报 + JSON 两种输出格式
- 配合 OpenClaw cron 可实现定时推送

## 数据源

[Open-Meteo API](https://open-meteo.com/)（开源免费，无需 API Key）

## 安装

```bash
# 方式1：直接 clone 到 OpenClaw skills 目录
git clone https://github.com/zixia0622/weather-push.git ~/.openclaw/skills/weather-push

# 方式2：下载 .skill 包（见 Releases）
```

安装后重启 OpenClaw gateway 生效：
```bash
openclaw gateway restart
```

## 使用

安装后直接对你的 Agent 说：

- "帮我查一下北京天气"
- "给我发今天上海的天气预报"
- "每天早上 8 点给我推送北京天气"

也可以直接运行脚本：

```bash
# 单城市
python3 ~/.openclaw/skills/weather-push/scripts/fetch_weather.py --city 北京

# 多城市
python3 ~/.openclaw/skills/weather-push/scripts/fetch_weather.py --cities 北京,上海,广州

# JSON 输出
python3 ~/.openclaw/skills/weather-push/scripts/fetch_weather.py --city 北京 --json
```

## 支持的城市

北京、上海、广州、深圳、成都、杭州、武汉、南京、西安、重庆、长沙、天津、苏州、郑州、厦门

其他城市可用 `--lat` `--lon` 经纬度参数。

## License

MIT
