#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片处理核心模块
"""

import os
from PIL import Image, UnidentifiedImageError
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

# 支持的图片格式
SUPPORTED_FORMATS = {
    # 必需格式
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.png': 'PNG',
    # 建议格式
    '.bmp': 'BMP',
    '.tiff': 'TIFF',
    '.tif': 'TIFF'
}


class ImageProcessor:
    """图片处理类"""
    
    @staticmethod
    def is_supported_format(file_path):
        """
        检查文件是否为支持的图片格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否支持
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in SUPPORTED_FORMATS
    
    @staticmethod
    def load_image(file_path):
        """
        加载图片文件
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            PIL.Image: 加载的图片对象
        """
        try:
            return Image.open(file_path)
        except Exception as e:
            print(f"加载图片失败: {e}")
            return None
    
    @staticmethod
    def pil_to_pixmap(pil_image):
        """
        将PIL图片转换为QPixmap
        
        Args:
            pil_image: PIL图片对象
            
        Returns:
            QPixmap: 转换后的QPixmap对象
        """
        if pil_image is None:
            return QPixmap()
            
        # 使用更高效的方式转换PIL图片为QImage
        if pil_image.mode == "RGBA":
            # 直接转换RGBA图像
            img_data = pil_image.tobytes("raw", "RGBA")
            img = QImage(img_data, pil_image.size[0], pil_image.size[1], 
                        pil_image.size[0] * 4, QImage.Format.Format_RGBA8888)
        else:
            # 其他模式统一转换为RGB
            pil_image = pil_image.convert("RGB")
            img_data = pil_image.tobytes("raw", "RGB")
            img = QImage(img_data, pil_image.size[0], pil_image.size[1], 
                        pil_image.size[0] * 3, QImage.Format.Format_RGB888)
            
        return QPixmap.fromImage(img)
    
    @staticmethod
    def create_thumbnail(pixmap, max_size=100):
        """
        创建缩略图
        
        Args:
            pixmap: 原始QPixmap对象
            max_size: 缩略图最大尺寸
            
        Returns:
            QPixmap: 缩略图QPixmap对象
        """
        # 使用FastTransformation代替SmoothTransformation以提高性能
        # 对于缩略图，牺牲一点质量换取速度是值得的
        return pixmap.scaled(max_size, max_size, 
                            Qt.AspectRatioMode.KeepAspectRatio, 
                            Qt.TransformationMode.FastTransformation)
    
    @staticmethod
    def get_image_info(file_path):
        """
        获取图片信息
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            dict: 包含图片信息的字典
        """
        try:
            img = Image.open(file_path)
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # KB
            
            return {
                "file_name": file_name,
                "file_path": file_path,
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_kb": round(file_size, 2)
            }
        except Exception as e:
            print(f"获取图片信息失败: {e}")
            return None