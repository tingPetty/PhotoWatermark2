#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PhotoWatermark2 - 一个简单易用的图片水印工具
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """主程序入口函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoWatermark2")
    app.setApplicationVersion("1.0.0")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 进入应用程序主循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()