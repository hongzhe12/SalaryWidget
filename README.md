# SalaryWidget：打工人财富增长可视化工具

## 项目简介
SalaryWidget 是一个基于 PySide6 开发的实时工资计算与可视化工具，旨在帮助用户直观了解工作时间与收入的动态关系。工具支持按秒计算薪资增长、显示每日/每月收入统计、进度条可视化今日目标完成度，并提供全局热键控制窗口显示/隐藏。

![QQ_1748861424710](https://github.com/user-attachments/assets/401be721-fa78-4b83-9c3b-484e77a3eba2)


## 功能特性
1. **实时薪资计算**
    - 基于配置的月薪、每月工作天数和每天工作小时数，自动计算每秒薪资速率。
    - 实时更新今日已赚金额、本月累计收入，并显示当前工作时间（小时:分钟:秒）。
2. **可视化界面**
    - 金色主题界面，包含标题、收入统计标签、进度条等元素。
    - 进度条显示今日收入目标完成度（基于日薪目标）。
    - 可拖动的无边框窗口，支持始终置顶显示。
3. **热键控制**
    - 默认热键 `]` 用于显示窗口，`Esc` 键用于隐藏窗口。
    - 可通过修改 `hotkey_manager.py` 中的 `start_listen` 方法自定义热键。
4. **配置管理**
    - 使用 YAML 配置文件 `config.yaml` 存储薪资参数（月薪、工作天数等）。
    - 支持动态修改配置并自动保存（需在 `conf_set.py` 中设置 `auto_save=True`）。

## 目录结构
```bash
SalaryWidget/
├── app.py # 主程序入口，包含界面逻辑和薪资计算
├── conf_set.py # 配置文件管理器，处理 YAML 配置读写
├── hotkey_manager.py # 全局热键管理类
├── main.py # 示例脚本（未使用，可忽略）
├── resources_rc.py # Qt 资源文件，包含图标 SVG 数据
├── test.py # 热键测试脚本
└── config.yaml # 配置文件（需手动创建，示例见下文）
```


## 依赖环境
- Python 3.8+
- PySide6 >= 6.9.0
- pynput >= 1.8.0
- PyYAML >= 6.0

## 安装与运行
### 1. 安装依赖
```bash
pip install pyside6 pynput pyyaml
```

薪资计算：在 update_salary 方法中，根据当前时间判断是否为工作日及工作时段，计算已工作秒数，进而得出今日收入和累计收入。
进度条更新：update_progress 方法根据今日收入与日薪目标的比例生成进度条，使用 QLinearGradient 实现金色渐变效果。
热键管理：通过 hotkey_manager.py 中的 Listener 监听全局键盘事件，触发信号控制窗口显示状态。
