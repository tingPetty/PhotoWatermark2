#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
事件处理模块
负责处理各种用户交互事件
"""

import os
from PyQt6.QtWidgets import QListWidget, QMessageBox, QWidget, QPushButton, QFileDialog, QColorDialog
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont, QFontMetrics, QPixmap, QColor

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
        
        # 新的文本水印功能事件
        self._setup_text_watermark_events()
        
        # 图片水印事件
        self._setup_image_watermark_events()
        
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
    
    def _setup_text_watermark_events(self):
        """设置文本水印相关事件"""
        # 字体选择
        if hasattr(self.main_window, 'font_combo'):
            self.main_window.font_combo.currentFontChanged.connect(self._update_font)
        
        # 字号
        if hasattr(self.main_window, 'font_size_spin'):
            self.main_window.font_size_spin.valueChanged.connect(self._update_font_size)
        
        # 粗体和斜体
        if hasattr(self.main_window, 'bold_checkbox'):
            self.main_window.bold_checkbox.toggled.connect(self._update_font_style)
        
        if hasattr(self.main_window, 'italic_checkbox'):
            self.main_window.italic_checkbox.toggled.connect(self._update_font_style)
        
        # 颜色选择
        if hasattr(self.main_window, 'color_button'):
            self.main_window.color_button.clicked.connect(self._select_text_color)
        
        # 样式效果
        if hasattr(self.main_window, 'shadow_checkbox'):
            self.main_window.shadow_checkbox.toggled.connect(self._update_text_shadow)
        
        if hasattr(self.main_window, 'stroke_checkbox'):
            self.main_window.stroke_checkbox.toggled.connect(self._update_text_stroke)
    
    def _update_font(self, font):
        """更新字体"""
        if not hasattr(self.main_window, 'text_font'):
            self.main_window.text_font = QFont()
        self.main_window.text_font.setFamily(font.family())
        self.main_window.watermark_handler.update_preview()
    
    def _update_font_size(self, size):
        """更新字号"""
        if not hasattr(self.main_window, 'text_font'):
            self.main_window.text_font = QFont()
        self.main_window.text_font.setPointSize(size)
        self.main_window.watermark_handler.update_preview()
    
    def _update_font_style(self):
        """更新字体样式（粗体、斜体）"""
        if not hasattr(self.main_window, 'text_font'):
            self.main_window.text_font = QFont()
        
        bold = self.main_window.bold_checkbox.isChecked() if hasattr(self.main_window, 'bold_checkbox') else False
        italic = self.main_window.italic_checkbox.isChecked() if hasattr(self.main_window, 'italic_checkbox') else False
        
        self.main_window.text_font.setBold(bold)
        self.main_window.text_font.setItalic(italic)
        self.main_window.watermark_handler.update_preview()
    
    def _select_text_color(self):
        """选择文本颜色"""
        current_color = getattr(self.main_window, 'text_color', QColor(0, 0, 0))
        color = QColorDialog.getColor(current_color, self.main_window, "选择文本颜色")
        
        if color.isValid():
            self.main_window.text_color = color
            # 更新颜色按钮的背景色
            self.main_window.color_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color.name()};
                    border: 1px solid #ccc;
                    border-radius: 3px;
                }}
                QPushButton:hover {{
                    border: 2px solid #666;
                }}
            """)
            self.main_window.watermark_handler.update_preview()
    
    def _update_text_shadow(self, enabled):
        """更新文本阴影效果"""
        self.main_window.text_shadow = enabled
        self.main_window.watermark_handler.update_preview()
    
    def _update_text_stroke(self, enabled):
        """更新文本描边效果"""
        self.main_window.text_stroke = enabled
        self.main_window.watermark_handler.update_preview()
    
    def _setup_image_watermark_events(self):
        """设置图片水印相关事件"""
        # 启用图片水印复选框
        if hasattr(self.main_window, 'enable_image_watermark'):
            self.main_window.enable_image_watermark.toggled.connect(self._toggle_image_watermark)
        
        # 图片选择按钮
        if hasattr(self.main_window, 'select_image_btn'):
            self.main_window.select_image_btn.clicked.connect(self._select_watermark_image)
        
        # 图片水印透明度滑块
        if hasattr(self.main_window, 'image_opacity_slider'):
            self.main_window.image_opacity_slider.valueChanged.connect(self._update_image_opacity)
        
        # 缩放控制
        if hasattr(self.main_window, 'proportional_scale'):
            self.main_window.proportional_scale.toggled.connect(self._toggle_proportional_scale)
        
        if hasattr(self.main_window, 'image_width_spin'):
            self.main_window.image_width_spin.valueChanged.connect(self._update_image_width)
        
        if hasattr(self.main_window, 'image_height_spin'):
            self.main_window.image_height_spin.valueChanged.connect(self._update_image_height)
    
    def _toggle_image_watermark(self, enabled):
        """切换图片水印启用状态"""
        self.main_window.image_watermark_enabled = enabled
        
        # 设置相关控件的启用状态
        self.main_window.ui_components.set_image_watermark_controls_enabled(enabled)
        
        self.main_window.watermark_handler.update_preview()
    
    def _select_watermark_image(self):
        """选择水印图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "选择水印图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif);;PNG文件 (*.png);;JPEG文件 (*.jpg *.jpeg)"
        )
        
        if file_path:
            # 加载图片并更新预览
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.main_window.watermark_image_path = file_path
                self.main_window.watermark_image = pixmap
                
                # 更新路径标签
                filename = os.path.basename(file_path)
                if len(filename) > 20:
                    filename = filename[:17] + "..."
                self.main_window.image_path_label.setText(filename)
                
                # 更新预览图片
                self._update_image_preview(pixmap)
                
                # 设置默认尺寸
                self.main_window.image_width_spin.setValue(min(100, pixmap.width()))
                self.main_window.image_height_spin.setValue(min(100, pixmap.height()))
                
                # 更新预览
                self.main_window.watermark_handler.update_preview()
            else:
                QMessageBox.warning(self.main_window, "错误", "无法加载选择的图片文件")
    
    def _update_image_preview(self, pixmap):
        """更新图片预览"""
        if pixmap and not pixmap.isNull():
            # 缩放图片以适应预览区域
            preview_size = 70
            scaled_pixmap = pixmap.scaled(
                preview_size, preview_size, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.main_window.image_preview_label.setPixmap(scaled_pixmap)
        else:
            self.main_window.image_preview_label.setText("图片预览")
            self.main_window.image_preview_label.setPixmap(QPixmap())
    
    def _update_image_opacity(self, value):
        """更新图片水印透明度"""
        self.main_window.image_watermark_opacity = value
        self.main_window.image_opacity_value.setText(f"{value}%")
        self.main_window.watermark_handler.update_preview()
    
    def _toggle_proportional_scale(self, enabled):
        """切换比例缩放模式"""
        self.main_window.proportional_scale_enabled = enabled
        if (enabled and hasattr(self.main_window, 'watermark_image') and 
            self.main_window.watermark_image is not None):
            # 如果启用比例缩放，根据当前宽度调整高度
            self._update_image_width(self.main_window.image_width_spin.value())
    
    def _update_image_width(self, width):
        """更新图片水印宽度"""
        self.main_window.image_watermark_width = width
        
        # 如果启用比例缩放，同时更新高度
        if (hasattr(self.main_window, 'proportional_scale_enabled') and 
            self.main_window.proportional_scale_enabled and 
            hasattr(self.main_window, 'watermark_image') and
            self.main_window.watermark_image is not None):
            
            original_width = self.main_window.watermark_image.width()
            original_height = self.main_window.watermark_image.height()
            
            if original_width > 0:
                new_height = int(width * original_height / original_width)
                self.main_window.image_height_spin.blockSignals(True)
                self.main_window.image_height_spin.setValue(new_height)
                self.main_window.image_height_spin.blockSignals(False)
                self.main_window.image_watermark_height = new_height
        
        self.main_window.watermark_handler.update_preview()
    
    def _update_image_height(self, height):
        """更新图片水印高度"""
        self.main_window.image_watermark_height = height
        
        # 如果启用比例缩放，同时更新宽度
        if (hasattr(self.main_window, 'proportional_scale_enabled') and 
            self.main_window.proportional_scale_enabled and 
            hasattr(self.main_window, 'watermark_image') and
            self.main_window.watermark_image is not None):
            
            original_width = self.main_window.watermark_image.width()
            original_height = self.main_window.watermark_image.height()
            
            if original_height > 0:
                new_width = int(height * original_width / original_height)
                self.main_window.image_width_spin.blockSignals(True)
                self.main_window.image_width_spin.setValue(new_width)
                self.main_window.image_width_spin.blockSignals(False)
                self.main_window.image_watermark_width = new_width
        
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
            
            # 连接导出图片动作
            if 'export_action' in self.main_window.menu_actions:
                self.main_window.menu_actions['export_action'].triggered.connect(
                    self.main_window.file_manager.export_current_image
                )
            
            # 连接批量导出动作
            if 'export_all_action' in self.main_window.menu_actions:
                self.main_window.menu_actions['export_all_action'].triggered.connect(
                    self.main_window.file_manager.export_all_images
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
            
            # 连接导出图片动作
            if 'export_action' in self.main_window.toolbar_actions:
                self.main_window.toolbar_actions['export_action'].triggered.connect(
                    self.main_window.file_manager.export_current_image
                )
            
            # 连接批量导出动作
            if 'export_all_action' in self.main_window.toolbar_actions:
                self.main_window.toolbar_actions['export_all_action'].triggered.connect(
                    self.main_window.file_manager.export_all_images
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