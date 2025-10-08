#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口类模块
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QStatusBar, QMenuBar, QToolBar, QFileDialog,
    QListWidget, QSplitter
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口基本属性
        self.setWindowTitle("PhotoWatermark2 - 图片水印工具")
        self.resize(1000, 700)
        
        # 初始化UI组件
        self._init_ui()
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        
    def _init_ui(self):
        """初始化UI布局"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧图片列表
        self.image_list = QListWidget()
        self.image_list.setMinimumWidth(200)
        splitter.addWidget(self.image_list)
        
        # 右侧区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 预览区域
        self.preview_area = QLabel("图片预览区域")
        self.preview_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_area.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ddd;")
        right_layout.addWidget(self.preview_area, 3)
        
        # 水印设置区域（占位）
        watermark_widget = QWidget()
        watermark_widget.setStyleSheet("background-color: #f8f8f8; border: 1px solid #ddd;")
        watermark_layout = QVBoxLayout(watermark_widget)
        watermark_layout.addWidget(QLabel("水印设置区域 (将在后续实现)"))
        right_layout.addWidget(watermark_widget, 1)
        
        splitter.addWidget(right_widget)
        
        # 设置分割器比例
        splitter.setSizes([200, 800])
        
        # 添加到主布局
        main_layout.addWidget(splitter)
        
    def _create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 打开图片动作
        open_action = QAction("打开图片", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_image)
        file_menu.addAction(open_action)
        
        # 保存图片动作
        save_action = QAction("保存图片", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        
        # 水印菜单
        watermark_menu = menu_bar.addMenu("水印")
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        
        # 关于动作
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)
        
    def _create_tool_bar(self):
        """创建工具栏"""
        tool_bar = QToolBar("主工具栏")
        tool_bar.setIconSize(QSize(16, 16))
        self.addToolBar(tool_bar)
        
        # 添加打开图片按钮
        open_action = QAction("打开图片", self)
        open_action.triggered.connect(self._open_image)
        tool_bar.addAction(open_action)
        
        # 添加保存图片按钮
        save_action = QAction("保存图片", self)
        tool_bar.addAction(save_action)
        
        tool_bar.addSeparator()
        
        # 添加水印按钮
        add_watermark_action = QAction("添加水印", self)
        tool_bar.addAction(add_watermark_action)
        
    def _create_status_bar(self):
        """创建状态栏"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # 添加状态信息
        self.status_label = QLabel("就绪")
        status_bar.addWidget(self.status_label)
        
    def _open_image(self):
        """打开图片对话框"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("图片文件 (*.jpg *.jpeg *.png *.bmp *.gif)")
        
        if file_dialog.exec():
            file_names = file_dialog.selectedFiles()
            self.status_label.setText(f"已选择 {len(file_names)} 个文件")
            # 这里后续会添加图片加载逻辑