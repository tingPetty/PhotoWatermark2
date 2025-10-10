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
    QPushButton, QGridLayout, QGroupBox, QFileDialog,
    QCheckBox, QSpinBox, QFrame, QComboBox, QColorDialog,
    QFontComboBox, QButtonGroup
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QFont, QColor, QFontDatabase


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
        text_layout.setSpacing(8)
        
        # 文本输入
        text_input_layout = QHBoxLayout()
        text_label = QLabel("水印文本:")
        text_label.setFixedWidth(60)
        text_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        text_input_layout.addWidget(text_label)
        
        self.main_window.text_input = QLineEdit(self.main_window.watermark_text)
        self.main_window.text_input.setStyleSheet(
            "QLineEdit { background-color: white; border: 1px solid #ccc; border-radius: 3px; padding: 3px; }"
        )
        self.main_window.text_input.setMinimumWidth(120)
        text_input_layout.addWidget(self.main_window.text_input)
        text_layout.addLayout(text_input_layout)
        
        # 字体设置区域
        font_layout = self._create_font_layout()
        text_layout.addLayout(font_layout)
        
        # 颜色和样式设置
        color_style_layout = self._create_color_style_layout()
        text_layout.addLayout(color_style_layout)
        
        # 透明度调节
        opacity_layout = self._create_opacity_layout()
        text_layout.addLayout(opacity_layout)
        
        text_group.setLayout(text_layout)
        return text_group
    
    def _create_font_layout(self):
        """创建字体设置布局"""
        font_main_layout = QVBoxLayout()
        font_main_layout.setSpacing(5)
        
        # 字体选择行
        font_row_layout = QHBoxLayout()
        font_label = QLabel("字体:")
        font_label.setFixedWidth(60)
        font_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        font_row_layout.addWidget(font_label)
        
        self.main_window.font_combo = QFontComboBox()
        self.main_window.font_combo.setCurrentFont(QFont("Arial"))
        self.main_window.font_combo.setStyleSheet("""
            QFontComboBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px;
                min-width: 80px;
            }
        """)
        font_row_layout.addWidget(self.main_window.font_combo)
        font_main_layout.addLayout(font_row_layout)
        
        # 字号和样式行
        size_style_layout = QHBoxLayout()
        size_label = QLabel("字号:")
        size_label.setFixedWidth(60)
        size_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        size_style_layout.addWidget(size_label)
        
        self.main_window.font_size_spin = QSpinBox()
        self.main_window.font_size_spin.setRange(8, 200)
        self.main_window.font_size_spin.setValue(18)
        self.main_window.font_size_spin.setFixedWidth(70)  # 增加宽度从50到70
        self.main_window.font_size_spin.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #ccc;
                border-bottom: 1px solid #ccc;
                border-top-right-radius: 3px;
                background-color: #f0f0f0;
            }
            QSpinBox::up-button:hover {
                background-color: #e0e0e0;
            }
            QSpinBox::up-button:pressed {
                background-color: #d0d0d0;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #ccc;
                border-top: 1px solid #ccc;
                border-bottom-right-radius: 3px;
                background-color: #f0f0f0;
            }
            QSpinBox::down-button:hover {
                background-color: #e0e0e0;
            }
            QSpinBox::down-button:pressed {
                background-color: #d0d0d0;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #666;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #666;
                width: 0px;
                height: 0px;
            }
        """)
        size_style_layout.addWidget(self.main_window.font_size_spin)
        
        # 添加间距
        size_style_layout.addSpacing(20)
        
        # 粗体复选框
        self.main_window.bold_checkbox = QCheckBox("粗体")
        self.main_window.bold_checkbox.setStyleSheet("""
            QCheckBox {
                border: none;
                background: transparent;
                font-size: 14px;
                font-weight: bold;
                spacing: 3px;
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
                border: 1px solid #ccc;
                border-radius: 2px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 1px solid #4CAF50;
            }
        """)
        size_style_layout.addWidget(self.main_window.bold_checkbox)
        
        # 斜体复选框
        self.main_window.italic_checkbox = QCheckBox("斜体")
        self.main_window.italic_checkbox.setStyleSheet("""
            QCheckBox {
                border: none;
                background: transparent;
                font-size: 14px;
                font-style: italic;
                spacing: 3px;
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
                border: 1px solid #ccc;
                border-radius: 2px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 1px solid #4CAF50;
            }
        """)
        size_style_layout.addWidget(self.main_window.italic_checkbox)
        
        font_main_layout.addLayout(size_style_layout)
        return font_main_layout
    
    def _create_color_style_layout(self):
        """创建颜色和样式设置布局"""
        color_style_layout = QVBoxLayout()
        color_style_layout.setSpacing(5)
        
        # 颜色选择行
        color_row_layout = QHBoxLayout()
        color_label = QLabel("颜色:")
        color_label.setFixedWidth(60)
        color_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        color_row_layout.addWidget(color_label)
        
        self.main_window.color_button = QPushButton()
        self.main_window.color_button.setFixedSize(30, 25)
        self.main_window.color_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton:hover {
                border: 2px solid #666;
            }
        """)
        color_row_layout.addWidget(self.main_window.color_button)
        
        # 增加颜色和效果之间的间距
        color_row_layout.addSpacing(60)
        
        # # 样式效果标签
        # style_label = QLabel("效果:")
        # style_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        # color_row_layout.addWidget(style_label)
        
        # # 在"效果"和"阴影"之间添加小间距
        # color_row_layout.addSpacing(5)
        
        # 阴影复选框
        self.main_window.shadow_checkbox = QCheckBox("阴影")
        self.main_window.shadow_checkbox.setStyleSheet("""
            QCheckBox {
                border: none;
                background: transparent;
                font-size: 14px;
                spacing: 3px;
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
                border: 1px solid #ccc;
                border-radius: 2px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 1px solid #4CAF50;
            }
        """)
        color_row_layout.addWidget(self.main_window.shadow_checkbox)
        
        # 描边复选框
        self.main_window.stroke_checkbox = QCheckBox("描边")
        self.main_window.stroke_checkbox.setStyleSheet("""
            QCheckBox {
                border: none;
                background: transparent;
                font-size: 14px;
                spacing: 3px;
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
                border: 1px solid #ccc;
                border-radius: 2px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 1px solid #4CAF50;
            }
        """)
        color_row_layout.addWidget(self.main_window.stroke_checkbox)
        
        color_style_layout.addLayout(color_row_layout)
        return color_style_layout
    
    def _create_opacity_layout(self):
        """创建透明度调节布局"""
        opacity_layout = QHBoxLayout()
        opacity_label = QLabel("透明度:")
        opacity_label.setFixedWidth(60)
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
        position_layout.setSpacing(8)  # 减小间距
        
        # 九宫格位置选择
        preset_label = QLabel("预设位置:")
        preset_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        position_layout.addWidget(preset_label)
        
        grid_layout = self._create_position_grid()
        position_layout.addLayout(grid_layout)
        
        # 拖拽提示
        hint_label = QLabel("提示: 您也可以直接在预览区域拖拽水印")
        hint_label.setStyleSheet("QLabel { border: none; background: transparent; color: #666; font-size: 12px; font-weight: bold; }")
        position_layout.addWidget(hint_label)
        
        # 旋转角度设置
        rotation_layout = self._create_rotation_layout()
        position_layout.addLayout(rotation_layout)
        
        position_group.setLayout(position_layout)
        return position_group
    
    def _create_position_grid(self):
        """创建九宫格位置选择"""
        grid_layout = QGridLayout()
        grid_layout.setSpacing(3)  # 减小间距从5到3
        positions = [
            (0, 0, "左上"), (0, 1, "上中"), (0, 2, "右上"),
            (1, 0, "左中"), (1, 1, "中心"), (1, 2, "右中"),
            (2, 0, "左下"), (2, 1, "下中"), (2, 2, "右下")
        ]
        
        for row, col, name in positions:
            btn = QPushButton(name)
            btn.setFixedSize(45, 25)  # 减小按钮尺寸从60x30到45x25
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
        """创建右侧水印区域（图片水印功能）"""
        right_watermark_area = QWidget()
        right_watermark_layout = QVBoxLayout(right_watermark_area)
        right_watermark_layout.setContentsMargins(5, 5, 5, 5)
        
        # 图片水印设置组
        image_group = self._create_image_watermark_group()
        right_watermark_layout.addWidget(image_group)
        
        # 添加弹性空间
        right_watermark_layout.addStretch(1)
        
        return right_watermark_area
    
    def _create_image_watermark_group(self):
        """创建图片水印设置组"""
        # 创建一个普通的Widget而不是QGroupBox，去掉标题和边框
        image_widget = QWidget()
        image_layout = QVBoxLayout()
        image_layout.setSpacing(10)
        
        # 启用图片水印复选框
        self.main_window.enable_image_watermark = QCheckBox("启用图片水印")
        self.main_window.enable_image_watermark.setChecked(False)  # 默认不选中
        self.main_window.enable_image_watermark.setStyleSheet("""
            QCheckBox {
                border: none;
                background: transparent;
                font-size: 12px;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 2px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
            QCheckBox::indicator:hover {
                border: 2px solid #81C784;
            }
        """)
        image_layout.addWidget(self.main_window.enable_image_watermark)
        
        # 图片选择区域
        image_select_layout = self._create_image_select_layout()
        image_layout.addLayout(image_select_layout)
        
        # 图片预览区域
        self.main_window.image_preview = self._create_image_preview()
        image_layout.addWidget(self.main_window.image_preview)
        
        # 缩放控制
        scale_layout = self._create_scale_layout()
        image_layout.addLayout(scale_layout)
        
        # 图片水印透明度调节
        image_opacity_layout = self._create_image_opacity_layout()
        image_layout.addLayout(image_opacity_layout)
        
        image_widget.setLayout(image_layout)
        return image_widget
    
    def _create_image_select_layout(self):
        """创建图片选择布局"""
        image_select_layout = QHBoxLayout()
        
        select_label = QLabel("选择图片:")
        select_label.setFixedWidth(70)
        select_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        image_select_layout.addWidget(select_label)
        
        self.main_window.select_image_btn = QPushButton("浏览...")
        self.main_window.select_image_btn.setFixedWidth(80)
        self.main_window.select_image_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        image_select_layout.addWidget(self.main_window.select_image_btn)
        
        self.main_window.image_path_label = QLabel("未选择图片")
        self.main_window.image_path_label.setStyleSheet(
            "QLabel { border: none; background: transparent; color: #666; }"
        )
        image_select_layout.addWidget(self.main_window.image_path_label)
        
        image_select_layout.addStretch(1)
        
        return image_select_layout
    
    def _create_image_preview(self):
        """创建图片预览区域"""
        preview_frame = QFrame()
        preview_frame.setFixedHeight(80)
        preview_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
        """)
        
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(5, 5, 5, 5)
        
        self.main_window.image_preview_label = QLabel("图片预览")
        self.main_window.image_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_window.image_preview_label.setStyleSheet(
            "QLabel { border: none; background: transparent; color: #999; }"
        )
        preview_layout.addWidget(self.main_window.image_preview_label)
        
        return preview_frame
    
    def _create_scale_layout(self):
        """创建缩放控制布局"""
        scale_layout = QVBoxLayout()
        
        # 缩放模式选择
        scale_mode_layout = QHBoxLayout()
        scale_mode_label = QLabel("缩放模式:")
        scale_mode_label.setFixedWidth(70)
        scale_mode_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        scale_mode_layout.addWidget(scale_mode_label)
        
        self.main_window.proportional_scale = QCheckBox("保持比例")
        self.main_window.proportional_scale.setChecked(False)  # 默认不选中，让用户自己选择
        self.main_window.proportional_scale.setStyleSheet("""
            QCheckBox {
                border: none;
                background: transparent;
                font-size: 12px;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
                border: 2px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
            QCheckBox::indicator:hover {
                border: 2px solid #81C784;
            }
        """)
        scale_mode_layout.addWidget(self.main_window.proportional_scale)
        
        scale_mode_layout.addStretch(1)
        scale_layout.addLayout(scale_mode_layout)
        
        # 缩放大小控制
        size_control_layout = QHBoxLayout()
        
        # 宽度控制
        width_label = QLabel("宽度:")
        width_label.setFixedWidth(35)
        width_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        size_control_layout.addWidget(width_label)
        
        self.main_window.image_width_spin = QSpinBox()
        self.main_window.image_width_spin.setRange(10, 1000)
        self.main_window.image_width_spin.setValue(100)
        self.main_window.image_width_spin.setSuffix("px")
        self.main_window.image_width_spin.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #ccc;
                border-bottom: 1px solid #ccc;
                border-top-right-radius: 3px;
                background-color: #f0f0f0;
            }
            QSpinBox::up-button:hover {
                background-color: #e0e0e0;
            }
            QSpinBox::up-button:pressed {
                background-color: #d0d0d0;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #ccc;
                border-top: 1px solid #ccc;
                border-bottom-right-radius: 3px;
                background-color: #f0f0f0;
            }
            QSpinBox::down-button:hover {
                background-color: #e0e0e0;
            }
            QSpinBox::down-button:pressed {
                background-color: #d0d0d0;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #666;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #666;
                width: 0px;
                height: 0px;
            }
        """)
        size_control_layout.addWidget(self.main_window.image_width_spin)
        
        # 高度控制
        height_label = QLabel("高度:")
        height_label.setFixedWidth(35)
        height_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        size_control_layout.addWidget(height_label)
        
        self.main_window.image_height_spin = QSpinBox()
        self.main_window.image_height_spin.setRange(10, 1000)
        self.main_window.image_height_spin.setValue(100)
        self.main_window.image_height_spin.setSuffix("px")
        self.main_window.image_height_spin.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #ccc;
                border-bottom: 1px solid #ccc;
                border-top-right-radius: 3px;
                background-color: #f0f0f0;
            }
            QSpinBox::up-button:hover {
                background-color: #e0e0e0;
            }
            QSpinBox::up-button:pressed {
                background-color: #d0d0d0;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #ccc;
                border-top: 1px solid #ccc;
                border-bottom-right-radius: 3px;
                background-color: #f0f0f0;
            }
            QSpinBox::down-button:hover {
                background-color: #e0e0e0;
            }
            QSpinBox::down-button:pressed {
                background-color: #d0d0d0;
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #666;
                width: 0px;
                height: 0px;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #666;
                width: 0px;
                height: 0px;
            }
        """)
        size_control_layout.addWidget(self.main_window.image_height_spin)
        
        size_control_layout.addStretch(1)
        scale_layout.addLayout(size_control_layout)
        
        return scale_layout
    
    def _create_image_opacity_layout(self):
        """创建图片水印透明度调节布局"""
        image_opacity_layout = QHBoxLayout()
        
        opacity_label = QLabel("透明度:")
        opacity_label.setFixedWidth(70)
        opacity_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        image_opacity_layout.addWidget(opacity_label)
        
        self.main_window.image_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.main_window.image_opacity_slider.setStyleSheet("""
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
                background: #4CAF50;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
                border: none;
            }
        """)
        self.main_window.image_opacity_slider.setRange(0, 100)
        self.main_window.image_opacity_slider.setValue(80)
        image_opacity_layout.addWidget(self.main_window.image_opacity_slider)
        
        self.main_window.image_opacity_value = QLabel("80%")
        self.main_window.image_opacity_value.setFixedWidth(40)
        image_opacity_layout.addWidget(self.main_window.image_opacity_value)
        
        return image_opacity_layout
    
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
        
        file_menu.addSeparator()
        
        # 导出图片动作
        export_action = QAction("导出图片", self.main_window)
        export_action.setShortcut("Ctrl+E")
        file_menu.addAction(export_action)
        
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
            'export_action': export_action,
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
        
        # 添加导出图片按钮
        export_action = QAction("导出图片", self.main_window)
        tool_bar.addAction(export_action)
        
        tool_bar.addSeparator()
        
        # 添加水印按钮
        add_watermark_action = QAction("添加水印", self.main_window)
        tool_bar.addAction(add_watermark_action)
        
        return {
            'open_action': open_action,
            'open_folder_action': open_folder_action,
            'remove_action': remove_action,
            'export_action': export_action,
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
    
    def set_image_watermark_controls_enabled(self, enabled):
        """设置图片水印相关控件的启用状态"""
        # 图片选择按钮
        if hasattr(self.main_window, 'select_image_btn'):
            self.main_window.select_image_btn.setEnabled(enabled)
        
        # 图片预览标签
        if hasattr(self.main_window, 'image_preview_label'):
            self.main_window.image_preview_label.setEnabled(enabled)
        
        # 保持比例复选框
        if hasattr(self.main_window, 'proportional_scale'):
            self.main_window.proportional_scale.setEnabled(enabled)
        
        # 宽度和高度输入框
        if hasattr(self.main_window, 'image_width_spin'):
            self.main_window.image_width_spin.setEnabled(enabled)
        if hasattr(self.main_window, 'image_height_spin'):
            self.main_window.image_height_spin.setEnabled(enabled)
        
        # 透明度滑块
        if hasattr(self.main_window, 'image_opacity_slider'):
            self.main_window.image_opacity_slider.setEnabled(enabled)
        
        # 设置控件的视觉效果（灰色蒙版效果）
        opacity = 1.0 if enabled else 0.4
        
        controls = [
            getattr(self.main_window, 'select_image_btn', None),
            getattr(self.main_window, 'image_preview_label', None),
            getattr(self.main_window, 'proportional_scale', None),
            getattr(self.main_window, 'image_width_spin', None),
            getattr(self.main_window, 'image_height_spin', None),
            getattr(self.main_window, 'image_opacity_slider', None)
        ]
        
        for control in controls:
            if control is not None:
                control.setStyleSheet(f"""
                    {control.styleSheet()}
                    opacity: {opacity};
                """)

    def _create_rotation_layout(self):
        """创建旋转角度控件布局"""
        rotation_layout = QHBoxLayout()
        rotation_label = QLabel("旋转角度:")
        rotation_label.setFixedWidth(60)
        rotation_label.setStyleSheet("QLabel { border: none; background: transparent; }")
        rotation_layout.addWidget(rotation_label)
        
        self.main_window.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.main_window.rotation_slider.setStyleSheet("""
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
        self.main_window.rotation_slider.setRange(0, 360)
        self.main_window.rotation_slider.setValue(self.main_window.watermark_rotation)
        rotation_layout.addWidget(self.main_window.rotation_slider)
        
        self.main_window.rotation_value = QLabel(f"{self.main_window.watermark_rotation}°")
        self.main_window.rotation_value.setFixedWidth(40)
        rotation_layout.addWidget(self.main_window.rotation_value)
        
        return rotation_layout