#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口类模块
"""

import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStatusBar
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

from core.image_processor import ImageProcessor
from ui.ui_components import UIComponents
from ui.event_handlers import EventHandlers
from ui.watermark_handler import WatermarkHandler
from ui.file_manager import FileManager


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口基本属性
        self.setWindowTitle("PhotoWatermark2 - 图片水印工具")
        self.resize(1000, 700)
        
        # 图片数据
        self.image_files = []  # 存储图片文件路径
        self.current_image = None  # 当前选中的图片
        
        # 水印数据
        self.watermark_text = "水印文本"  # 默认水印文本
        self.watermark_opacity = 50  # 默认透明度 (0-100)
        self.watermark_position = QPoint(50, 50)  # 默认位置
        self.is_dragging = False  # 是否正在拖拽水印
        
        # 新的文本水印属性
        from PyQt6.QtGui import QFont, QColor
        self.text_font = QFont("Arial", 24)  # 默认字体
        self.text_color = QColor(0, 0, 0)  # 默认黑色
        self.text_shadow = False  # 阴影效果
        self.text_stroke = False  # 描边效果
        
        # 图片水印数据
        self.image_watermark_enabled = False  # 是否启用图片水印
        self.watermark_image_path = ""  # 水印图片路径
        self.watermark_image = None  # 水印图片QPixmap对象
        self.image_watermark_width = 100  # 图片水印宽度
        self.image_watermark_height = 100  # 图片水印高度
        self.image_watermark_opacity = 80  # 图片水印透明度 (0-100)
        self.proportional_scale_enabled = False  # 是否启用比例缩放，默认关闭
        self.image_watermark_position = QPoint(10, 10)  # 图片水印位置
        
        # 初始化组件管理器
        self.ui_components = UIComponents(self)
        self.watermark_handler = WatermarkHandler(self)
        self.file_manager = FileManager(self)
        self.event_handlers = EventHandlers(self)
        
        # 初始化UI
        self._init_ui()
        
        # 启用拖放功能
        self.setAcceptDrops(True)
        
    def _init_ui(self):
        """初始化用户界面"""
        # 创建中央部件
        self.ui_components.create_central_widget()
        
        # 创建菜单栏并保存动作对象
        self.menu_actions = self.ui_components.create_menu_bar()
        
        # 创建工具栏并保存动作对象
        self.toolbar_actions = self.ui_components.create_tool_bar()
        
        # 创建状态栏
        self.ui_components.create_status_bar()
        
        # 设置事件处理
        self.event_handlers.setup_event_connections()
        
        # 初始化图片水印控件状态（默认禁用）
        self.ui_components.set_image_watermark_controls_enabled(False)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        self.event_handlers.drag_enter_event(event)
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件"""
        self.event_handlers.drop_event(event)
    
    def get_watermark_rect(self):
        """获取水印矩形区域"""
        return self.watermark_handler.get_watermark_rect()
    
    def update_preview(self):
        """更新预览"""
        self.watermark_handler.update_preview()
    
    # 为了保持向后兼容性，保留一些原有的方法名
    def _open_image(self):
        """打开图片"""
        self.file_manager.open_image_dialog()
    
    def _open_folder(self):
        """打开文件夹"""
        self.file_manager.open_folder_dialog()
    
    def _remove_selected_images(self):
        """删除选中的图片"""
        self.file_manager.remove_selected_images()
    
    def _save_current_image(self):
        """保存当前图片"""
        self.file_manager.save_current_image()
    
    def _save_all_images(self):
        """批量保存所有图片"""
        self.file_manager.save_all_images()