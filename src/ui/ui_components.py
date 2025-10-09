#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI组件创建模块
负责创建和配置各种UI组件
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QStatusBar, QMenuBar, QToolBar, 
    QListWidget, QSplitter, QLineEdit, QSlider, 
    QPushButton, QGridLayout, QGroupBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction


class UIComponents:
    """UI组件创建和管理类"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def create_central_widget(self):
        """创建中央部件和主布局"""
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧图片列表
        self.main_window.image_list = self._create_image_list()
        splitter.addWidget(self.main_window.image_list)
        
        # 右侧区域
        right_widget = self._create_right_widget()
        splitter.addWidget(right_widget)
        
        # 设置分割器比例
        splitter.setSizes([200, 800])
        
        # 添加到主布局
        main_layout.addWidget(splitter)
        
        return central_widget
    
    def _create_image_list(self):
        """创建图片列表组件"""
        image_list = QListWidget()
        image_list.setMinimumWidth(200)
        image_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        return image_list
    
    def _create_right_widget(self):
        """创建右侧区域组件"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 预览区域
        self.main_window.preview_area = self._create_preview_area()
        right_layout.addWidget(self.main_window.preview_area, 3)
        
        # 水印设置区域
        watermark_widget = self._create_watermark_widget()
        right_layout.addWidget(watermark_widget, 1)
        
        return right_widget
    
    def _create_preview_area(self):
        """创建预览区域"""
        preview_area = QLabel("图片预览区域")
        preview_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_area.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ddd;")
        return preview_area
    
    def _create_watermark_widget(self):
        """创建水印设置区域"""
        watermark_widget = QWidget()
        watermark_widget.setStyleSheet("background-color: #f8f8f8; border: 1px solid #ddd;")
        watermark_layout = QHBoxLayout(watermark_widget)
        
        # 左侧水印设置区域
        left_watermark_area = self._create_left_watermark_area()
        watermark_layout.addWidget(left_watermark_area)
        
        # 右侧区域（预留空间）
        right_watermark_area = self._create_right_watermark_area()
        watermark_layout.addWidget(right_watermark_area)
        
        # 设置左右区域的比例为1:1
        watermark_layout.setStretch(0, 1)
        watermark_layout.setStretch(1, 1)
        
        return watermark_widget
    
    def _create_left_watermark_area(self):
        """创建左侧水印设置区域"""
        left_watermark_area = QWidget()
        left_watermark_layout = QVBoxLayout(left_watermark_area)
        left_watermark_layout.setContentsMargins(5, 5, 5, 5)
        
        # 文本水印设置
        text_group = self._create_text_watermark_group()
        left_watermark_layout.addWidget(text_group)
        
        # 位置调整
        position_group = self._create_position_group()
        left_watermark_layout.addWidget(position_group)
        
        # 添加弹性空间
        left_watermark_layout.addStretch(1)
        
        return left_watermark_area
    
    def _create_text_watermark_group(self):
        """创建文本水印设置组"""
        text_group = QGroupBox()
        text_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        text_layout = QVBoxLayout()
        text_layout.setSpacing(10)
        
        # 文本输入
        text_input_layout = QHBoxLayout()
        text_label = QLabel("水印文本:")
        text_label.setFixedWidth(70)
        text_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        text_input_layout.addWidget(text_label)
        
        self.main_window.text_input = QLineEdit(self.main_window.watermark_text)
        self.main_window.text_input.setStyleSheet(
            "QLineEdit { background-color: white; border: 1px solid #ccc; border-radius: 3px; padding: 3px; }"
        )
        self.main_window.text_input.setMinimumWidth(150)
        text_input_layout.addWidget(self.main_window.text_input)
        text_layout.addLayout(text_input_layout)
        
        # 透明度调节
        opacity_layout = self._create_opacity_layout()
        text_layout.addLayout(opacity_layout)
        
        text_group.setLayout(text_layout)
        return text_group
    
    def _create_opacity_layout(self):
        """创建透明度调节布局"""
        opacity_layout = QHBoxLayout()
        opacity_label = QLabel("透明度:")
        opacity_label.setFixedWidth(70)
        opacity_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        opacity_layout.addWidget(opacity_label)
        
        self.main_window.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.main_window.opacity_slider.setStyleSheet("""
            QSlider {
                border: none;
                background: transparent;
            }
            QSlider::groove:horizontal {
                background: #e0e0e0;
                height: 8px;
                border-radius: 4px;
                border: none;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
                border: none;
            }
        """)
        self.main_window.opacity_slider.setRange(0, 100)
        self.main_window.opacity_slider.setValue(self.main_window.watermark_opacity)
        opacity_layout.addWidget(self.main_window.opacity_slider)
        
        self.main_window.opacity_value = QLabel(f"{self.main_window.watermark_opacity}%")
        self.main_window.opacity_value.setFixedWidth(40)
        opacity_layout.addWidget(self.main_window.opacity_value)
        
        return opacity_layout
    
    def _create_position_group(self):
        """创建位置调整组"""
        position_group = QGroupBox()
        position_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        position_layout = QVBoxLayout()
        position_layout.setSpacing(10)
        
        # 九宫格位置选择
        preset_label = QLabel("预设位置:")
        preset_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        position_layout.addWidget(preset_label)
        
        grid_layout = self._create_position_grid()
        position_layout.addLayout(grid_layout)
        
        # 拖拽提示
        hint_label = QLabel("提示: 您也可以直接在预览区域拖拽水印")
        hint_label.setStyleSheet("QLabel { border: none; background: transparent; color: #666; }")
        position_layout.addWidget(hint_label)
        
        position_group.setLayout(position_layout)
        return position_group
    
    def _create_position_grid(self):
        """创建九宫格位置选择"""
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        positions = [
            (0, 0, "左上"), (0, 1, "上中"), (0, 2, "右上"),
            (1, 0, "左中"), (1, 1, "中心"), (1, 2, "右中"),
            (2, 0, "左下"), (2, 1, "下中"), (2, 2, "右下")
        ]
        
        for row, col, name in positions:
            btn = QPushButton(name)
            btn.setFixedSize(60, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
                QPushButton:pressed {
                    background-color: #d4d4d4;
                }
            """)
            # 注意：这里需要在main_window中连接信号
            btn.setProperty("position", (row, col))
            grid_layout.addWidget(btn, row, col)
        
        return grid_layout
    
    def _create_right_watermark_area(self):
        """创建右侧水印区域（预留空间）"""
        right_watermark_area = QWidget()
        right_watermark_layout = QVBoxLayout(right_watermark_area)
        right_watermark_layout.addStretch(1)
        return right_watermark_area
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.main_window.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 打开图片动作
        open_action = QAction("打开图片", self.main_window)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        # 打开文件夹动作
        open_folder_action = QAction("打开文件夹", self.main_window)
        open_folder_action.setShortcut("Ctrl+Shift+O")
        file_menu.addAction(open_folder_action)
        
        # 保存图片动作
        save_action = QAction("保存图片", self.main_window)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction("退出", self.main_window)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        
        # 水印菜单
        watermark_menu = menu_bar.addMenu("水印")
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        
        # 关于动作
        about_action = QAction("关于", self.main_window)
        help_menu.addAction(about_action)
        
        return {
            'open_action': open_action,
            'open_folder_action': open_folder_action,
            'save_action': save_action,
            'exit_action': exit_action,
            'about_action': about_action
        }
    
    def create_tool_bar(self):
        """创建工具栏"""
        tool_bar = QToolBar("主工具栏")
        tool_bar.setIconSize(QSize(16, 16))
        self.main_window.addToolBar(tool_bar)
        
        # 添加打开图片按钮
        open_action = QAction("打开图片", self.main_window)
        tool_bar.addAction(open_action)
        
        # 添加打开文件夹按钮
        open_folder_action = QAction("打开文件夹", self.main_window)
        tool_bar.addAction(open_folder_action)
        
        # 添加删除图片按钮
        remove_action = QAction("删除图片", self.main_window)
        tool_bar.addAction(remove_action)
        
        # 添加保存图片按钮
        save_action = QAction("保存图片", self.main_window)
        tool_bar.addAction(save_action)
        
        tool_bar.addSeparator()
        
        # 添加水印按钮
        add_watermark_action = QAction("添加水印", self.main_window)
        tool_bar.addAction(add_watermark_action)
        
        return {
            'open_action': open_action,
            'open_folder_action': open_folder_action,
            'remove_action': remove_action,
            'save_action': save_action,
            'add_watermark_action': add_watermark_action
        }
    
    def create_status_bar(self):
        """创建状态栏"""
        status_bar = QStatusBar()
        self.main_window.setStatusBar(status_bar)
        
        # 添加状态信息
        self.main_window.status_label = QLabel("就绪")
        status_bar.addWidget(self.main_window.status_label)
        
        return status_bar