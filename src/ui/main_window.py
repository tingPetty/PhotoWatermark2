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
from ui.template_manager import TemplateManager


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口基本属性
        self.setWindowTitle("PhotoWatermark2 - 图片水印工具")
        self.resize(1000, 900)
        
        # 图片数据
        self.image_files = []  # 存储图片文件路径
        self.current_image = None  # 当前选中的图片
        
        # 水印数据
        self.watermark_text = "水印文本"
        self.watermark_position = QPoint(50, 50)
        self.watermark_opacity = 80  # 透明度 (0-100)
        self.watermark_rotation = 0  # 旋转角度 (0-360)
        self.is_dragging = False  # 是否正在拖拽水印
        
        # 新的文本水印属性
        from PyQt6.QtGui import QFont, QColor
        self.text_font = QFont("Arial", 24)  # 默认字体
        self.text_color = QColor(0, 0, 0)  # 默认黑色
        self.text_shadow = False  # 阴影效果
        self.text_stroke = False  # 描边效果
        self.stroke_color = QColor(255, 255, 255)  # 默认白色描边
        
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
        
        # 自动加载上次的设置
        self._load_last_settings()
        
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
    
    def _load_last_settings(self):
        """加载上次的设置"""
        try:
            template_manager = TemplateManager()
            last_settings = template_manager.load_last_settings()
            
            if last_settings:
                # 应用设置到界面
                self._apply_settings_to_ui(last_settings)
        except Exception as e:
            print(f"加载上次设置失败: {e}")
    
    def _apply_settings_to_ui(self, settings):
        """将设置应用到界面"""
        from PyQt6.QtGui import QFont, QColor
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QPixmap
        
        # 应用文本水印设置
        if 'text' in settings and hasattr(self, 'text_input'):
            self.text_input.setText(settings['text'])
            self.watermark_text = settings['text']
        
        if 'font_family' in settings and hasattr(self, 'font_combo'):
            font = QFont(settings['font_family'])
            self.font_combo.setCurrentFont(font)
            self.text_font.setFamily(settings['font_family'])
        
        if 'font_size' in settings and hasattr(self, 'font_size_spin'):
            self.font_size_spin.setValue(settings['font_size'])
            self.text_font.setPointSize(settings['font_size'])
        
        if 'bold' in settings and hasattr(self, 'bold_btn'):
            self.bold_btn.setChecked(settings['bold'])
            self.text_font.setBold(settings['bold'])
        
        if 'italic' in settings and hasattr(self, 'italic_btn'):
            self.italic_btn.setChecked(settings['italic'])
            self.text_font.setItalic(settings['italic'])
        
        if 'text_color' in settings:
            color_data = settings['text_color']
            self.text_color = QColor(color_data[0], color_data[1], color_data[2], color_data[3])
            # 更新颜色按钮显示
            if hasattr(self, 'color_button'):
                self.color_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.text_color.name()};
                        border: 1px solid #ccc;
                        border-radius: 3px;
                    }}
                    QPushButton:hover {{
                        border: 2px solid #666;
                    }}
                """)
        
        # 应用图片水印设置
        if 'image_path' in settings and settings['image_path']:
            self.watermark_image_path = settings['image_path']
            # 更新图片显示
            if hasattr(self, 'image_preview'):
                pixmap = QPixmap(settings['image_path'])
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    self.image_preview.setPixmap(scaled_pixmap)
                    self.watermark_image = pixmap
        
        if 'image_size' in settings and hasattr(self, 'image_size_spin'):
            self.image_size_spin.setValue(settings['image_size'])
            self.image_watermark_width = settings['image_size']
            self.image_watermark_height = settings['image_size']
        
        # 应用通用设置
        if 'opacity' in settings and hasattr(self, 'opacity_slider'):
            self.opacity_slider.setValue(settings['opacity'])
            self.watermark_opacity = settings['opacity']
        
        if 'position' in settings:
            if isinstance(settings['position'], list) and len(settings['position']) == 2:
                self.watermark_position = QPoint(settings['position'][0], settings['position'][1])
            elif hasattr(settings['position'], 'x') and hasattr(settings['position'], 'y'):
                self.watermark_position = settings['position']
        
        if 'rotation' in settings and hasattr(self, 'rotation_slider'):
            self.watermark_rotation = settings['rotation']
            self.rotation_slider.setValue(settings['rotation'])
            # 更新显示值
            if hasattr(self, 'rotation_value'):
                self.rotation_value.setText(f"{settings['rotation']}°")
    
    def closeEvent(self, event):
        """窗口关闭事件，保存当前设置"""
        try:
            # 获取当前设置
            current_settings = self._get_current_settings()
            
            # 保存为上次设置
            template_manager = TemplateManager()
            template_manager.save_last_settings(current_settings)
        except Exception as e:
            print(f"保存设置失败: {e}")
        
        # 调用父类的关闭事件
        super().closeEvent(event)
    
    def _get_current_settings(self):
        """获取当前设置"""
        settings = {}
        
        # 文本水印设置
        if hasattr(self, 'text_input'):
            settings['text'] = self.text_input.text()
        
        if hasattr(self, 'font_combo'):
            settings['font_family'] = self.font_combo.currentFont().family()
        
        if hasattr(self, 'font_size_spin'):
            settings['font_size'] = self.font_size_spin.value()
        
        if hasattr(self, 'bold_btn'):
            settings['bold'] = self.bold_btn.isChecked()
        
        if hasattr(self, 'italic_btn'):
            settings['italic'] = self.italic_btn.isChecked()
        
        if hasattr(self, 'text_color'):
            color = self.text_color
            settings['text_color'] = [color.red(), color.green(), color.blue(), color.alpha()]
        
        # 图片水印设置
        if hasattr(self, 'watermark_image_path'):
            settings['image_path'] = self.watermark_image_path
        
        if hasattr(self, 'image_size_spin'):
            settings['image_size'] = self.image_size_spin.value()
        
        # 通用设置
        if hasattr(self, 'opacity_slider'):
            settings['opacity'] = self.opacity_slider.value()
        
        if hasattr(self, 'watermark_position'):
            settings['position'] = [self.watermark_position.x(), self.watermark_position.y()]
        
        if hasattr(self, 'watermark_rotation'):
            settings['rotation'] = self.watermark_rotation
        
        return settings