#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
水印处理模块
负责水印的渲染和相关逻辑
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter

from core.image_processor import ImageProcessor


class WatermarkHandler:
    """水印处理类"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def update_preview(self, force_resize=False):
        """更新预览区域，显示带水印的图片"""
        if not self.main_window.current_image:
            return
            
        # 加载原始图片
        image = ImageProcessor.load_image(self.main_window.current_image)
        if not image:
            return
            
        pixmap = ImageProcessor.pil_to_pixmap(image)
        
        # 检查是否需要重新计算尺寸
        current_pixmap = self.main_window.preview_area.pixmap()
        should_resize = force_resize or not current_pixmap or current_pixmap.isNull()
        
        if should_resize:
            # 重新计算适合预览区域的尺寸
            preview_size = self.main_window.preview_area.size()
            scaled_pixmap = pixmap.scaled(
                preview_size.width(), 
                preview_size.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            # 保持当前尺寸，仅更新水印
            scaled_pixmap = pixmap.scaled(
                current_pixmap.width(), 
                current_pixmap.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        
        # 创建一个新的QPixmap用于绘制水印
        result_pixmap = QPixmap(scaled_pixmap)
        painter = QPainter(result_pixmap)
        
        # 设置字体和颜色
        font = QFont("Arial", 20, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))  # 设置黑色文本
        
        # 设置透明度
        painter.setOpacity(self.main_window.watermark_opacity / 100.0)
        
        # 绘制水印文本
        painter.drawText(
            self.main_window.watermark_position.x(), 
            self.main_window.watermark_position.y(), 
            self.main_window.watermark_text
        )
        
        painter.end()
        
        # 显示带水印的图片
        self.main_window.preview_area.setPixmap(result_pixmap)
    
    def apply_watermark_to_image(self, image_path, output_path=None):
        """将水印应用到指定图片并保存"""
        # 加载原始图片
        image = ImageProcessor.load_image(image_path)
        if not image:
            return False
            
        # 转换为QPixmap
        pixmap = ImageProcessor.pil_to_pixmap(image)
        
        # 计算水印位置的缩放比例
        # 获取当前预览图片的尺寸
        current_preview_pixmap = self.main_window.preview_area.pixmap()
        if current_preview_pixmap and not current_preview_pixmap.isNull():
            # 计算从预览尺寸到原始尺寸的缩放比例
            scale_x = pixmap.width() / current_preview_pixmap.width()
            scale_y = pixmap.height() / current_preview_pixmap.height()
            
            # 根据缩放比例调整水印位置
            watermark_x = int(self.main_window.watermark_position.x() * scale_x)
            watermark_y = int(self.main_window.watermark_position.y() * scale_y)
        else:
            # 如果无法获取预览尺寸，使用原始位置
            watermark_x = self.main_window.watermark_position.x()
            watermark_y = self.main_window.watermark_position.y()
        
        # 创建一个新的QPixmap用于绘制水印
        result_pixmap = QPixmap(pixmap)
        painter = QPainter(result_pixmap)
        
        # 设置字体和颜色（需要根据原始图片尺寸调整字体大小）
        if current_preview_pixmap and not current_preview_pixmap.isNull():
            # 根据缩放比例调整字体大小
            font_size = int(20 * max(scale_x, scale_y))
        else:
            font_size = 20
            
        font = QFont("Arial", font_size, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))  # 设置黑色文本
        
        # 设置透明度
        painter.setOpacity(self.main_window.watermark_opacity / 100.0)
        
        # 绘制水印文本
        painter.drawText(watermark_x, watermark_y, self.main_window.watermark_text)
        
        painter.end()
        
        # 保存图片
        if output_path:
            return result_pixmap.save(output_path)
        else:
            # 如果没有指定输出路径，覆盖原文件
            return result_pixmap.save(image_path)
    
    def get_watermark_preview(self, image_path):
        """获取带水印的图片预览（不保存）"""
        # 加载原始图片
        image = ImageProcessor.load_image(image_path)
        if not image:
            return None
            
        # 转换为QPixmap
        pixmap = ImageProcessor.pil_to_pixmap(image)
        
        # 创建一个新的QPixmap用于绘制水印
        result_pixmap = QPixmap(pixmap)
        painter = QPainter(result_pixmap)
        
        # 设置字体和颜色
        font = QFont("Arial", 20, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))  # 设置黑色文本
        
        # 设置透明度
        painter.setOpacity(self.main_window.watermark_opacity / 100.0)
        
        # 绘制水印文本
        painter.drawText(
            self.main_window.watermark_position.x(), 
            self.main_window.watermark_position.y(), 
            self.main_window.watermark_text
        )
        
        painter.end()
        
        return result_pixmap