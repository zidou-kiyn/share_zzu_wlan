# Share ZZU WLAN - 郑州大学移动校园宽带共享工具

![ZZU WLAN](https://img.shields.io/badge/ZZU-WLAN-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**在那些漫长的夜晚，当你的舍友流量耗尽，当实验室的访客无法连接网络，当你想在多设备间自由切换...**

Share ZZU WLAN 来了！这是一款专为郑州大学学子打造的移动校园宽带共享神器，让你的移动校园宽带账号不再受设备限制的束缚。

## 🌟 功能特点

- **自动认证**：一键完成移动校园宽带认证，告别繁琐的手动登录
- **多账号支持**：突破设备绑定限制，让多个账号共享同一移动校园宽带
- **跨平台兼容**：不仅支持Windows，还可在任何支持Python的平台上运行
- **简单易用**：小白也能轻松上手的操作流程

## 🚀 快速开始

### 前提条件

- 你需要有郑州大学中国移动校园卡
- 该卡已绑定校园宽带
- 你的设备已连接到`ZZU-WLAN`这个WiFi

### 安装步骤

1. 克隆本仓库或下载ZIP包到本地
   ```bash
   git clone https://github.com/your-username/share_zzu_wlan.git
   ```

2. 配置你的账号信息
   - 将`config.json.example`重命名为`config.json`
   - 或直接运行程序，它会自动生成配置文件模板

3. 编辑`config.json`，填入你的信息：
   ```json
   {
       "username": "你的统一认证账号",
       "password": "你的统一认证密码",
       "operator": "@cmcc",
       "phone": "你的移动校园卡手机号"
   }
   ```

4. 运行程序
   - **Python方式**：
     ```bash
     pip install -r requirements.txt
     python main.py
     ```
   - **可执行文件方式**：双击运行`main.exe`

## 📱 跨平台使用

不只是Windows，你还可以在各种平台上使用本工具：

- **Android手机**：安装Pydroid 3应用，导入项目并运行
- **Linux/Mac**：和Windows下的Python使用方法一样
- **其他设备**：只要能运行Python，就能使用本工具

## 🔧 进阶使用

- 设置开机自启动，永远不再为认证烦恼
- 结合任务计划，定时检查网络状态并自动重连


## ⚠️ 免责声明

**本项目在2025年3月9日及之前均可正常使用，但不对之后的可用性做任何保证。**

校园网认证系统可能随时变更，本工具可能因此失效。项目仅供学习交流使用，请勿用于任何违反校规校纪或法律法规的行为。使用本工具产生的任何后果由使用者自行承担。

## 🤔 常见问题

**Q: 为什么配置正确但无法连接？**  
A: 请检查是否已连接ZZU-WLAN，以及校园网系统是否处于维护状态。

**Q: 可以同时给多少设备共享？**  
A: 理论上没有限制，但移动校园宽带的带宽是共享的,请合理使用，避免影响他人网络体验。

**Q: 这会影响我的账号安全吗？**  
A: 本工具仅在本地存储账号信息，不会上传任何数据。但请不要将配置文件分享给他人。

## 🔄 更新日志

- v1.0.0 (2025-03-09): 首次发布，支持基本认证功能

## 🤝 贡献

欢迎提交Issue和Pull Request！一起让这个工具变得更好。

## 📜 许可证

MIT License © 2025

---

*"网络不再是束缚，而是自由的翅膀。" —— Share ZZU WLAN*