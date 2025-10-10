#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
水印处理模块
负责水印的渲染和相关逻辑
"""

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter, QPen
import os

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
        
        # 绘制文本水印
        if self.main_window.watermark_text:
            self._draw_text_watermark(painter)
        
        # 绘制图片水印
        if hasattr(self.main_window, 'image_watermark_enabled') and self.main_window.image_watermark_enabled:
            if hasattr(self.main_window, 'watermark_image_path') and self.main_window.watermark_image_path:
                self._draw_image_watermark(painter, scaled_pixmap.size())
        
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
        
        # 绘制文本水印
        if self.main_window.watermark_text:
            if current_preview_pixmap and not current_preview_pixmap.isNull():
                self._draw_text_watermark_scaled(painter, watermark_x, watermark_y, scale_x, scale_y)
            else:
                # 保存原始位置，临时设置新位置
                original_pos = self.main_window.watermark_position
                self.main_window.watermark_position = QPoint(watermark_x, watermark_y)
                self._draw_text_watermark(painter)
                self.main_window.watermark_position = original_pos
        
        # 绘制图片水印
        if hasattr(self.main_window, 'image_watermark_enabled') and self.main_window.image_watermark_enabled:
            if hasattr(self.main_window, 'watermark_image_path') and self.main_window.watermark_image_path:
                # 计算图片水印的缩放比例
                if current_preview_pixmap and not current_preview_pixmap.isNull():
                    self._draw_image_watermark_scaled(painter, pixmap.size(), scale_x, scale_y)
                else:
                    self._draw_image_watermark(painter, pixmap.size())
        
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
        
        # 绘制文本水印
        if self.main_window.watermark_text:
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
        
        # 绘制图片水印
        if hasattr(self.main_window, 'image_watermark_enabled') and self.main_window.image_watermark_enabled:
            if hasattr(self.main_window, 'watermark_image_path') and self.main_window.watermark_image_path:
                self._draw_image_watermark(painter, pixmap.size())
        
        painter.end()
        
        return result_pixmap
    
    def _draw_image_watermark(self, painter, canvas_size):
        """绘制图片水印"""
        if not hasattr(self.main_window, 'watermark_image_path') or not self.main_window.watermark_image_path:
            return
            
        if not os.path.exists(self.main_window.watermark_image_path):
            return
            
        # 加载水印图片
        watermark_pixmap = QPixmap(self.main_window.watermark_image_path)
        if watermark_pixmap.isNull():
            return
            
        # 获取缩放设置
        if hasattr(self.main_window, 'image_watermark_width') and hasattr(self.main_window, 'image_watermark_height'):
            target_width = self.main_window.image_watermark_width
            target_height = self.main_window.image_watermark_height
            
            # 如果启用了比例缩放，保持宽高比
            if hasattr(self.main_window, 'proportional_scale_enabled') and self.main_window.proportional_scale_enabled:
                # 计算缩放比例，保持宽高比
                scale_x = target_width / watermark_pixmap.width()
                scale_y = target_height / watermark_pixmap.height()
                scale = min(scale_x, scale_y)
                
                scaled_width = int(watermark_pixmap.width() * scale)
                scaled_height = int(watermark_pixmap.height() * scale)
            else:
                scaled_width = target_width
                scaled_height = target_height
                
            # 缩放水印图片
            watermark_pixmap = watermark_pixmap.scaled(
                scaled_width, scaled_height,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        
        # 获取透明度设置
        opacity = 1.0
        if hasattr(self.main_window, 'image_watermark_opacity'):
            opacity = self.main_window.image_watermark_opacity / 100.0
            
        # 设置透明度
        painter.setOpacity(opacity)
        
        # 计算水印位置（默认右上角）
        watermark_x = canvas_size.width() - watermark_pixmap.width() - 10
        watermark_y = 10
        
        # 如果有自定义位置，使用自定义位置
        if hasattr(self.main_window, 'image_watermark_position'):
            watermark_x = self.main_window.image_watermark_position.x()
            watermark_y = self.main_window.image_watermark_position.y()
        
        # 绘制水印图片
        painter.drawPixmap(watermark_x, watermark_y, watermark_pixmap)
        
        # 恢复透明度
        painter.setOpacity(1.0)
    
    def _draw_text_watermark(self, painter):
        """绘制文本水印，支持字体、颜色和样式效果"""
        # 设置字体
        painter.setFont(self.main_window.text_font)
        
        # 设置透明度
        painter.setOpacity(self.main_window.watermark_opacity / 100.0)
        
        # 获取文本位置
        x = self.main_window.watermark_position.x()
        y = self.main_window.watermark_position.y()
        text = self.main_window.watermark_text
        
        # 根据样式效果绘制文本
        # 先绘制阴影效果（如果启用）
        if hasattr(self.main_window, 'text_shadow') and self.main_window.text_shadow:
            shadow_color = QColor(128, 128, 128, 180)  # 半透明灰色阴影
            painter.setPen(shadow_color)
            painter.drawText(x + 2, y + 2, text)  # 阴影偏移2像素
        
        # 再绘制描边效果（如果启用）
        if hasattr(self.main_window, 'text_stroke') and self.main_window.text_stroke:
            stroke_pen = QPen(QColor(255, 255, 255), 2)  # 白色描边，2像素宽度
            painter.setPen(stroke_pen)
            painter.drawText(x, y, text)
        
        # 最后绘制主文本
        painter.setPen(self.main_window.text_color)
        painter.drawText(x, y, text)
    
    def _draw_text_watermark_scaled(self, painter, x, y, scale_x, scale_y):
        """绘制缩放后的文本水印（用于导出）"""
        # 创建缩放后的字体
        scaled_font = QFont(self.main_window.text_font)
        original_size = self.main_window.text_font.pointSize()
        scaled_size = int(original_size * max(scale_x, scale_y))
        scaled_font.setPointSize(scaled_size)
        
        # 设置字体
        painter.setFont(scaled_font)
        
        # 设置透明度
        painter.setOpacity(self.main_window.watermark_opacity / 100.0)
        
        # 获取文本
        text = self.main_window.watermark_text
        
        # 根据样式效果绘制文本
        # 先绘制阴影效果（如果启用）
        if hasattr(self.main_window, 'text_shadow') and self.main_window.text_shadow:
            # 绘制阴影效果（阴影偏移也需要缩放）
            shadow_offset = int(2 * max(scale_x, scale_y))
            shadow_color = QColor(128, 128, 128, 180)
            painter.setPen(shadow_color)
            painter.drawText(x + shadow_offset, y + shadow_offset, text)
        
        # 再绘制描边效果（如果启用）
        if hasattr(self.main_window, 'text_stroke') and self.main_window.text_stroke:
            # 绘制描边效果（描边宽度也需要缩放）
            stroke_width = int(2 * max(scale_x, scale_y))
            stroke_pen = QPen(QColor(255, 255, 255), stroke_width)
            painter.setPen(stroke_pen)
            painter.drawText(x, y, text)
        
        # 最后绘制主文本
        painter.setPen(self.main_window.text_color)
        painter.drawText(x, y, text)
    
    def _draw_image_watermark_scaled(self, painter, canvas_size, scale_x, scale_y):
        """绘制缩放后的图片水印（用于导出）"""
        if not hasattr(self.main_window, 'watermark_image_path') or not self.main_window.watermark_image_path:
            return
            
        if not os.path.exists(self.main_window.watermark_image_path):
            return
            
        # 加载水印图片
        watermark_pixmap = QPixmap(self.main_window.watermark_image_path)
        if watermark_pixmap.isNull():
            return
            
        # 获取缩放设置并应用导出缩放比例
        if hasattr(self.main_window, 'image_watermark_width') and hasattr(self.main_window, 'image_watermark_height'):
            target_width = int(self.main_window.image_watermark_width * scale_x)
            target_height = int(self.main_window.image_watermark_height * scale_y)
            
            # 如果启用了比例缩放，保持宽高比
            if hasattr(self.main_window, 'proportional_scale_enabled') and self.main_window.proportional_scale_enabled:
                # 计算缩放比例，保持宽高比
                scale_ratio_x = target_width / watermark_pixmap.width()
                scale_ratio_y = target_height / watermark_pixmap.height()
                scale_ratio = min(scale_ratio_x, scale_ratio_y)
                
                scaled_width = int(watermark_pixmap.width() * scale_ratio)
                scaled_height = int(watermark_pixmap.height() * scale_ratio)
            else:
                scaled_width = target_width
                scaled_height = target_height
                
            # 缩放水印图片
            watermark_pixmap = watermark_pixmap.scaled(
                scaled_width, scaled_height,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        
        # 获取透明度设置
        opacity = 1.0
        if hasattr(self.main_window, 'image_watermark_opacity'):
            opacity = self.main_window.image_watermark_opacity / 100.0
            
        # 设置透明度
        painter.setOpacity(opacity)
        
        # 计算水印位置（默认右上角，应用缩放）
        watermark_x = int((canvas_size.width() - watermark_pixmap.width() - 10))
        watermark_y = int(10 * scale_y)
        
        # 如果有自定义位置，使用自定义位置并应用缩放
        if hasattr(self.main_window, 'image_watermark_position'):
            watermark_x = int(self.main_window.image_watermark_position.x() * scale_x)
            watermark_y = int(self.main_window.image_watermark_position.y() * scale_y)
        
        # 绘制水印图片
        painter.drawPixmap(watermark_x, watermark_y, watermark_pixmap)
        
        # 恢复透明度
        painter.setOpacity(1.0)