#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
事件处理模块
负责处理各种用户交互事件
"""

import os
from PyQt6.QtWidgets import QListWidget, QMessageBox, QWidget, QPushButton
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont, QFontMetrics

from core.image_processor import ImageProcessor


class EventHandlers:
    """事件处理类"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def setup_event_connections(self):
        """设置所有事件连接"""
        # 图片列表事件
        self.main_window.image_list.itemClicked.connect(self._on_image_selected)
        self.main_window.image_list.keyPressEvent = self._list_key_press_event
        
        # 预览区域鼠标事件
        self.main_window.preview_area.mousePressEvent = self._preview_mouse_press
        self.main_window.preview_area.mouseMoveEvent = self._preview_mouse_move
        self.main_window.preview_area.mouseReleaseEvent = self._preview_mouse_release
        
        # 水印设置事件
        self.main_window.text_input.textChanged.connect(self._update_watermark_text)
        self.main_window.opacity_slider.valueChanged.connect(self._update_watermark_opacity)
        
        # 连接九宫格位置按钮
        self._connect_position_buttons()
        
        # 连接菜单栏和工具栏事件
        self._connect_menu_actions()
        self._connect_toolbar_actions()
        
    def _connect_position_buttons(self):
        """连接九宫格位置按钮的事件"""
        # 查找所有位置按钮并连接事件
        watermark_widget = self.main_window.centralWidget().findChild(QWidget)
        if watermark_widget:
            buttons = watermark_widget.findChildren(QPushButton)
            for btn in buttons:
                position = btn.property("position")
                if position:
                    row, col = position
                    btn.clicked.connect(lambda checked, r=row, c=col: self._set_preset_position(r, c))
    
    def _on_image_selected(self, item):
        """图片选择事件处理"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.main_window.current_image = file_path
        
        # 更新预览，强制重新计算尺寸
        self.main_window.watermark_handler.update_preview(force_resize=True)
        
        # 更新状态栏
        image_info = ImageProcessor.get_image_info(file_path)
        self.main_window.status_label.setText(
            f"当前图片: {os.path.basename(file_path)} - "
            f"{image_info['width']}x{image_info['height']} - "
            f"{image_info['format']} - {image_info['size_kb']}KB"
        )
    
    def _list_key_press_event(self, event):
        """处理图片列表的键盘事件"""
        # 处理Delete键删除图片
        if event.key() == Qt.Key.Key_Delete:
            self.main_window.file_manager.remove_selected_images()
        else:
            # 调用原始的keyPressEvent方法处理其他键盘事件
            QListWidget.keyPressEvent(self.main_window.image_list, event)
    
    def _update_watermark_text(self, text):
        """更新水印文本"""
        self.main_window.watermark_text = text
        self.main_window.watermark_handler.update_preview()
        
    def _update_watermark_opacity(self, value):
        """更新水印透明度"""
        self.main_window.watermark_opacity = value
        self.main_window.opacity_value.setText(f"{value}%")
        self.main_window.watermark_handler.update_preview()
        
    def _set_preset_position(self, row, col):
        """设置预设位置"""
        if not self.main_window.current_image:
            return
            
        # 获取当前显示的图片尺寸
        pixmap = self.main_window.preview_area.pixmap()
        if not pixmap:
            return
            
        # 直接使用pixmap的尺寸，因为水印是绘制在pixmap上的
        pixmap_width = pixmap.width()
        pixmap_height = pixmap.height()
        
        # 创建字体对象来计算文本尺寸
        font = QFont("Arial", 20, QFont.Weight.Bold)
        font_metrics = QFontMetrics(font)
        text_rect = font_metrics.boundingRect(self.main_window.watermark_text)
        text_width = text_rect.width()
        text_height = text_rect.height()
        
        # 计算九宫格位置，考虑文本尺寸以实现真正的居中
        padding_ratio = 0.05  # 边缘填充比例
        
        # 计算左中右三个水平位置
        if col == 0:  # 左
            x_pos = pixmap_width * padding_ratio
        elif col == 1:  # 中
            x_pos = (pixmap_width - text_width) / 2
        else:  # 右 (col == 2)
            x_pos = pixmap_width * (1 - padding_ratio) - text_width
        
        # 计算上中下三个垂直位置
        if row == 0:  # 上
            y_pos = pixmap_height * padding_ratio + text_height
        elif row == 1:  # 中
            y_pos = (pixmap_height + text_height) / 2
        else:  # 下 (row == 2)
            y_pos = pixmap_height * (1 - padding_ratio)

        self.main_window.watermark_position = QPoint(int(x_pos), int(y_pos))
        self.main_window.watermark_handler.update_preview()
    
    def _preview_mouse_press(self, event):
        """处理预览区域的鼠标按下事件"""
        if not self.main_window.current_image:
            return
            
        # 检查是否点击在水印文本区域
        text_rect = self._get_watermark_rect()
        if text_rect.contains(event.position().toPoint()):
            self.main_window.is_dragging = True
            self.main_window.drag_start_pos = event.position().toPoint()
            self.main_window.original_watermark_pos = QPoint(self.main_window.watermark_position)
            
    def _preview_mouse_move(self, event):
        """处理预览区域的鼠标移动事件"""
        if not self.main_window.is_dragging:
            return
            
        # 获取当前显示的pixmap
        pixmap = self.main_window.preview_area.pixmap()
        if not pixmap:
            return
            
        # 计算预览区域的缩放比例
        preview_rect = self.main_window.preview_area.contentsRect()
        if pixmap.width() / pixmap.height() > preview_rect.width() / preview_rect.height():
            scale = preview_rect.width() / pixmap.width()
        else:
            scale = preview_rect.height() / pixmap.height()
        
        # 计算在预览区域中的移动距离
        delta_in_preview = event.position().toPoint() - self.main_window.drag_start_pos
        
        # 将预览区域的移动距离转换为pixmap坐标系的移动距离
        delta_in_pixmap = QPoint(
            int(delta_in_preview.x() / scale),
            int(delta_in_preview.y() / scale)
        )
        
        # 更新水印位置（在pixmap坐标系中）
        self.main_window.watermark_position = self.main_window.original_watermark_pos + delta_in_pixmap
        
        # 更新预览
        self.main_window.watermark_handler.update_preview()
        
    def _preview_mouse_release(self, event):
        """处理预览区域的鼠标释放事件"""
        self.main_window.is_dragging = False
        
    def _get_watermark_rect(self):
        """获取水印文本的矩形区域"""
        if not self.main_window.current_image:
            return QRect()
            
        # 获取当前显示的pixmap
        pixmap = self.main_window.preview_area.pixmap()
        if not pixmap:
            return QRect()
            
        # 计算文本尺寸
        font = QFont("Arial", 20, QFont.Weight.Bold)
        font_metrics = QFontMetrics(font)
        text_rect = font_metrics.boundingRect(self.main_window.watermark_text)
        text_width = text_rect.width()
        text_height = text_rect.height()
        
        # 计算pixmap在预览区域中的显示位置和尺寸
        preview_rect = self.main_window.preview_area.contentsRect()
        pixmap_rect = pixmap.rect()
        
        # 计算缩放比例和偏移
        if pixmap.width() / pixmap.height() > preview_rect.width() / preview_rect.height():
            # 按宽度缩放
            scale = preview_rect.width() / pixmap.width()
            scaled_width = preview_rect.width()
            scaled_height = int(pixmap.height() * scale)
            x_offset = 0
            y_offset = (preview_rect.height() - scaled_height) // 2
        else:
            # 按高度缩放
            scale = preview_rect.height() / pixmap.height()
            scaled_height = preview_rect.height()
            scaled_width = int(pixmap.width() * scale)
            y_offset = 0
            x_offset = (preview_rect.width() - scaled_width) // 2
        
        # 将pixmap坐标系中的水印位置转换为预览区域坐标系
        watermark_x_in_preview = x_offset + self.main_window.watermark_position.x() * scale
        watermark_y_in_preview = y_offset + self.main_window.watermark_position.y() * scale
        
        # 创建水印文本的矩形区域（注意：drawText的y坐标是基线，需要调整）
        text_left = watermark_x_in_preview
        text_top = watermark_y_in_preview - text_height
        text_rect_in_preview = QRect(
            int(text_left), 
            int(text_top), 
            int(text_width * scale), 
            int(text_height * scale)
        )
        
        # 扩大点击区域，使其更容易选中
        text_rect_in_preview.adjust(-10, -10, 10, 10)
        
        return text_rect_in_preview
    
    # 拖放事件处理
    def drag_enter_event(self, event: QDragEnterEvent):
        """拖拽进入事件处理"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def drop_event(self, event: QDropEvent):
        """拖拽放下事件处理"""
        file_paths = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isdir(file_path):
                # 如果是文件夹，处理文件夹
                self.main_window.file_manager.process_folder(file_path)
            elif ImageProcessor.is_supported_format(file_path):
                # 如果是支持的图片格式
                file_paths.append(file_path)
        
        if file_paths:
            self.main_window.file_manager.load_images(file_paths)
            self.main_window.status_label.setText(f"已导入 {len(file_paths)} 个图片文件")
    
    def _connect_menu_actions(self):
        """连接菜单栏动作事件"""
        if hasattr(self.main_window, 'menu_actions'):
            # 连接打开图片动作
            if 'open_action' in self.main_window.menu_actions:
                self.main_window.menu_actions['open_action'].triggered.connect(
                    self.main_window.file_manager.open_image_dialog
                )
            
            # 连接打开文件夹动作
            if 'open_folder_action' in self.main_window.menu_actions:
                self.main_window.menu_actions['open_folder_action'].triggered.connect(
                    self.main_window.file_manager.open_folder_dialog
                )
            
            # 连接保存图片动作
            if 'save_action' in self.main_window.menu_actions:
                self.main_window.menu_actions['save_action'].triggered.connect(
                    self.main_window.file_manager.save_current_image
                )
    
    def _connect_toolbar_actions(self):
        """连接工具栏动作事件"""
        if hasattr(self.main_window, 'toolbar_actions'):
            # 连接打开图片动作
            if 'open_action' in self.main_window.toolbar_actions:
                self.main_window.toolbar_actions['open_action'].triggered.connect(
                    self.main_window.file_manager.open_image_dialog
                )
            
            # 连接打开文件夹动作
            if 'open_folder_action' in self.main_window.toolbar_actions:
                self.main_window.toolbar_actions['open_folder_action'].triggered.connect(
                    self.main_window.file_manager.open_folder_dialog
                )
            
            # 连接删除图片动作
            if 'remove_action' in self.main_window.toolbar_actions:
                self.main_window.toolbar_actions['remove_action'].triggered.connect(
                    self.main_window.file_manager.remove_selected_images
                )
            
            # 连接保存图片动作
            if 'save_action' in self.main_window.toolbar_actions:
                self.main_window.toolbar_actions['save_action'].triggered.connect(
                    self.main_window.file_manager.save_current_image
                )
            
            # 连接添加水印动作
            if 'add_watermark_action' in self.main_window.toolbar_actions:
                self.main_window.toolbar_actions['add_watermark_action'].triggered.connect(
                    self._apply_watermark_to_current
                )
    
    def _apply_watermark_to_current(self):
        """对当前图片应用水印"""
        if self.main_window.current_image:
            self.main_window.watermark_handler.apply_watermark_to_image(
                self.main_window.current_image
            )