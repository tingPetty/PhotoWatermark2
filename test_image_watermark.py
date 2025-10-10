#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图片水印功能测试脚本
"""

import sys
import os
from PIL import Image, ImageDraw

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_test_images():
    """创建测试图片"""
    # 创建测试目录
    test_dir = "test_imagewatermark"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # 创建一个简单的测试图片
    img = Image.new('RGB', (400, 300), color='lightblue')
    draw = ImageDraw.Draw(img)
    draw.text((150, 140), "测试图片", fill='black')
    img.save(os.path.join(test_dir, "test_photo.jpg"))
    
    # 创建一个带透明通道的PNG水印图片
    watermark = Image.new('RGBA', (100, 50), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark)
    # 绘制一个半透明的矩形
    draw.rectangle([10, 10, 90, 40], fill=(255, 0, 0, 128), outline=(0, 0, 0, 255))
    draw.text((25, 20), "LOGO", fill=(255, 255, 255, 255))
    watermark.save(os.path.join(test_dir, "logo_watermark.png"))
    
    print(f"测试图片已创建在 {test_dir} 目录中:")
    print("- test_photo.jpg: 测试照片")
    print("- logo_watermark.png: 带透明通道的水印图片")

if __name__ == "__main__":
    create_test_images()