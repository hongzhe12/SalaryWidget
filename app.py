import sys
from calendar import calendar

from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                               QHBoxLayout)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QLinearGradient, QIcon
from datetime import datetime, timedelta

from conf_set import config_instance
from hotkey_manager import HotkeyManager
import resources_rc


class SalaryWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口图标（使用资源路径）
        self.setWindowIcon(QIcon(":/icon/柯基.svg"))  # 使用 `:/别名` 访问资源

        # 工资参数设置
        self.monthly_salary = config_instance.get('月薪')  # 月薪(元)
        self.work_days_per_month = config_instance.get('每月工作天数')  # 每月工作天数
        self.work_hours_per_day = config_instance.get('每天工作小时数')  # 每天工作小时数

        # 计算每秒工资
        self.salary_per_second = self.monthly_salary / (self.work_days_per_month *
                                                        self.work_hours_per_day *
                                                        3600)

        # 设置窗口属性
        self.setWindowTitle("💰 打工人财富增长可视化")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(400, 450)

        # 创建UI
        self.init_ui()

        # 设置定时器更新金额
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_salary)
        self.timer.start(100)  # 每秒更新一次

        # 初始更新
        self.update_salary()

        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.hotkey_pressed.connect(self.on_hotkey_pressed)
        self.hotkey_manager.esc_pressed.connect(self.hide)
        self.hotkey_manager.start_listen(']')

    def on_hotkey_pressed(self):
        self.show()
        print('热键已触发')

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 顶部标题
        self.title_label = QLabel("💻 数字游民收入仪表盘")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Microsoft YaHei', 16, QFont.Bold))

        # 月薪累计收入
        self.monthly_total_label = QLabel("📈 本月累计: ¥0.00")
        self.monthly_total_label.setAlignment(Qt.AlignCenter)
        self.monthly_total_label.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))

        # 今日赚得
        self.daily_label = QLabel("💰 今日赚得: ¥0.00")
        self.daily_label.setAlignment(Qt.AlignCenter)
        self.daily_label.setFont(QFont('Microsoft YaHei', 20, QFont.Bold))

        # 实时金额显示
        self.amount_label = QLabel("⚡ 实时速率: ¥0.00/秒")
        self.amount_label.setAlignment(Qt.AlignCenter)
        self.amount_label.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))

        # 工作时间显示
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont('Microsoft YaHei', 12))

        # 统计信息
        stats_layout = QHBoxLayout()
        self.stats_left = QLabel()
        self.stats_left.setAlignment(Qt.AlignLeft)
        self.stats_left.setFont(QFont('Microsoft YaHei', 10))
        self.stats_right = QLabel()
        self.stats_right.setAlignment(Qt.AlignRight)
        self.stats_right.setFont(QFont('Microsoft YaHei', 10))
        stats_layout.addWidget(self.stats_left)
        stats_layout.addWidget(self.stats_right)

        # 进度条容器
        self.progress_container = QWidget()
        self.progress_container.setFixedHeight(20)

        # 调整后的布局顺序
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.monthly_total_label)  # 月薪累计在上
        main_layout.addWidget(self.daily_label)  # 今日赚得在中
        main_layout.addWidget(self.amount_label)  # 实时速率在下
        main_layout.addWidget(self.time_label)
        main_layout.addSpacing(10)
        main_layout.addLayout(stats_layout)
        main_layout.addWidget(self.progress_container)

        self.setLayout(main_layout)

        # 设置样式 - 金色主题
        self.setStyleSheet("""
            QLabel {
                margin: 5px;
            }
            #title_label {
                color: #FFD700;
                font-size: 18px;
                padding-bottom: 10px;
                background-color: rgba(20, 15, 0, 150);
                border-radius: 15px;
            }
            #monthly_total_label {
                color: #FFD700;
                font-size: 18px;
                background-color: rgba(40, 30, 0, 180);
                border-radius: 15px;
                padding: 10px;
                border: 1px solid #FFD700;
            }
            #daily_label {
                color: #FFD700;
                font-size: 20px;
                background-color: rgba(40, 30, 0, 180);
                border-radius: 15px;
                padding: 10px;
                border: 1px solid #FFD700;
            }
            #amount_label {
                color: #FFD700;
                font-size: 18px;
                background-color: rgba(40, 30, 0, 180);
                border-radius: 15px;
                padding: 10px;
                border: 1px solid #FFD700;
            }
            #time_label {
                color: #FFD700;
                font-size: 14px;
                background-color: rgba(40, 30, 0, 120);
                border-radius: 8px;
                padding: 5px;
            }
            #stats_left, #stats_right {
                color: #FFD700;
                background-color: rgba(40, 30, 0, 150);
                border-radius: 8px;
                padding: 5px;
                border: 1px solid #FFD700;
            }
            #progress_container {
                background-color: rgba(40, 30, 0, 150); 
                border-radius: 10px;
                border: 1px solid #FFD700;
            }
        """)

    def update_salary(self):
        try:
            # now = datetime.now() - timedelta(days=3)
            now = datetime.now()
            # 计算本月已工作天数（包括今天）
            work_days_so_far = sum(
                1 for day in range(1, now.day + 1)
                if datetime(now.year, now.month, day).weekday() < 5
            )

            # 判断今天是否为工作日（周一=0，周五=4）
            is_workday = now.weekday() < 5

            # 设定工作时间段（09:00-17:00）
            work_start = now.replace(hour=9, minute=0, second=0, microsecond=0)
            work_end = now.replace(hour=17, minute=0, second=0, microsecond=0)

            # 计算今日工作时间（秒）
            if not is_workday:
                worked_seconds = 0
            elif now < work_start:
                worked_seconds = 0
            elif now > work_end:
                worked_seconds = (work_end - work_start).total_seconds()
            else:
                worked_seconds = (now - work_start).total_seconds()

            # 计算收入
            today_earned = self.salary_per_second * worked_seconds
            monthly_earned = (self.monthly_salary / self.work_days_per_month) * work_days_so_far

            # 如果是工作日且在工作时段内，加上今日收入
            if is_workday and worked_seconds > 0:
                monthly_earned += today_earned

            # 格式化显示
            today_earned_str = f"{today_earned:,.3f}"
            monthly_earned_str = f"{monthly_earned:,.3f}"
            current_rate = f"{self.salary_per_second:.3f}"

            # 工作时间显示
            hours, remainder = divmod(int(worked_seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            # 计算今日目标进度
            target_per_day = self.monthly_salary / self.work_days_per_month
            progress = min(100, (today_earned / target_per_day) * 100) if is_workday else 0

            # 更新UI
            self.monthly_total_label.setText(f"📈 本月累计: ¥{monthly_earned_str}")
            self.daily_label.setText(f"💰 今日赚得: ¥{today_earned_str}")
            self.amount_label.setText(f"⚡ 实时速率: ¥{current_rate}/秒")
            self.time_label.setText(f"⏱️ 工作时间: {time_str}" if is_workday else "🎉 休息日")

            # 更新统计信息
            self.stats_left.setText(
                f"🤑 时薪: ¥{self.monthly_salary / self.work_days_per_month / self.work_hours_per_day:.2f}\n"
                f"📅 日薪: ¥{self.monthly_salary / self.work_days_per_month:.2f}")

            self.stats_right.setText(
                f"🏦 月薪: ¥{self.monthly_salary:.2f}\n"
                f"💼 工作天数: {self.work_days_per_month}天/月")

            self.update_progress(progress)

        except Exception as e:
            print(f"工资计算错误: {e}")
            # 可以在这里添加错误恢复逻辑

    def update_progress(self, progress):
        # 清除旧的进度条
        for child in self.progress_container.children():
            if isinstance(child, QWidget):
                child.deleteLater()

        # 创建新的进度条
        progress_bar = QWidget(self.progress_container)
        progress_width = int(self.progress_container.width() * progress / 100)
        progress_bar.setGeometry(0, 0, progress_width, self.progress_container.height())

        # 设置金色渐变进度条
        progress_bar.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                         stop:0 #FFD700, stop:1 #FFA500);
            border-radius: 10px;
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景和边框
        rect = self.rect()
        rect.adjust(1, 1, -1, -1)

        # 绘制半透明圆角背景 (金色主题)
        painter.setPen(Qt.NoPen)
        ''' 0 = 完全透明
            255 = 完全不透明
            180 = 约70%不透明度（推荐值）
            120 = 约50%不透明度
        '''
        painter.setBrush(QColor(40, 30, 0, 0))  # 深金色背景 #
        painter.drawRoundedRect(rect, 20, 20)

        # 绘制金色边框
        gradient = QLinearGradient(rect.topLeft(), rect.topRight())
        gradient.setColorAt(0, QColor(255, 215, 0))  # 金色
        gradient.setColorAt(1, QColor(255, 165, 0))  # 橙色

        pen = QPen(QBrush(gradient), 3)  # 3像素宽的金色渐变边框
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 20, 20)


if __name__ == "__main__":
    try:
        from ctypes import windll  # Only exists on Windows.

        myappid = 'mycompany.myproduct.subproduct.version'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icon/柯基.svg"))

    # 设置全局字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    widget = SalaryWidget()
    widget.show()

    sys.exit(app.exec())
