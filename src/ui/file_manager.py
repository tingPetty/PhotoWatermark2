#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件管理模块
负责处理图片文件的打开、保存、导出等操作
"""

import os
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from core.image_processor import ImageProcessor
from .dialogs import ExportDialog


class FileManager:
    """文件管理类"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def open_image_dialog(self):
        """打开图片对话框"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("图片文件 (*.jpg *.jpeg *.png *.bmp *.gif)")
        
        if file_dialog.exec():
            file_names = file_dialog.selectedFiles()
            self.main_window.status_label.setText(f"已选择 {len(file_names)} 个文件")
            self.load_images(file_names)
    
    def open_folder_dialog(self):
        """打开文件夹对话框"""
        folder_path = QFileDialog.getExistingDirectory(self.main_window, "选择图片文件夹")
        if folder_path:
            self.process_folder(folder_path)
    
    def load_images(self, file_paths):
        """加载图片文件"""
        for file_path in file_paths:
            # 检查文件是否已经在列表中
            if file_path in self.main_window.image_files:
                continue
                
            # 获取图片信息
            image_info = ImageProcessor.get_image_info(file_path)
            if not image_info:
                QMessageBox.warning(self.main_window, "警告", f"无法加载图片: {file_path}")
                continue
                
            # 添加到图片文件列表
            self.main_window.image_files.append(file_path)
            
            # 创建缩略图
            image = ImageProcessor.load_image(file_path)
            if not image:
                continue
                
            pixmap = ImageProcessor.pil_to_pixmap(image)
            thumbnail = ImageProcessor.create_thumbnail(pixmap)
            
            # 创建列表项
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.ItemDataRole.UserRole, file_path)  # 存储文件路径
            item.setIcon(QIcon(thumbnail))
            item.setToolTip(f"{image_info['width']}x{image_info['height']} - {image_info['size_kb']}KB")
            
            # 添加到列表
            self.main_window.image_list.addItem(item)
        
        # 如果有图片，选择第一个
        if self.main_window.image_list.count() > 0 and not self.main_window.current_image:
            self.main_window.image_list.setCurrentRow(0)
            first_item = self.main_window.image_list.item(0)
            if first_item:
                self.main_window.event_handlers._on_image_selected(first_item)
    
    def process_folder(self, folder_path):
        """处理文件夹中的图片"""
        image_count = 0
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if ImageProcessor.is_supported_format(file_path):
                    self.load_images([file_path])
                    image_count += 1
        
        self.main_window.status_label.setText(f"从文件夹导入了 {image_count} 个图片文件")
    
    def remove_selected_images(self):
        """删除选中的图片"""
        selected_items = self.main_window.image_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            row = self.main_window.image_list.row(item)
            file_path = item.data(Qt.ItemDataRole.UserRole)
            
            # 从列表中移除
            self.main_window.image_list.takeItem(row)
            
            # 从文件列表中移除
            if file_path in self.main_window.image_files:
                self.main_window.image_files.remove(file_path)
                
        # 更新状态栏
        self.main_window.status_label.setText(f"已删除 {len(selected_items)} 个图片")
        
        # 如果当前没有选中的图片，清空预览区域
        if self.main_window.image_list.count() == 0:
            self.main_window.preview_area.clear()
            self.main_window.current_image = None
        elif self.main_window.image_list.currentItem():
            current_item = self.main_window.image_list.currentItem()
            if current_item:
                self.main_window.event_handlers._on_image_selected(current_item)
    
    def save_current_image(self, output_path=None):
        """保存当前图片（带水印）"""
        if not self.main_window.current_image:
            QMessageBox.warning(self.main_window, "警告", "请先选择一张图片")
            return False
            
        if not output_path:
            # 如果没有指定输出路径，弹出保存对话框
            output_path, _ = QFileDialog.getSaveFileName(
                self.main_window,
                "保存图片",
                os.path.splitext(self.main_window.current_image)[0] + "_watermarked.jpg",
                "图片文件 (*.jpg *.jpeg *.png *.bmp)"
            )
            
        if output_path:
            success = self.main_window.watermark_handler.apply_watermark_to_image(
                self.main_window.current_image, 
                output_path
            )
            if success:
                self.main_window.status_label.setText(f"图片已保存到: {output_path}")
                return True
            else:
                QMessageBox.critical(self.main_window, "错误", "保存图片失败")
                return False
        
        return False
    
    def save_all_images(self, output_folder=None):
        """批量保存所有图片（带水印）"""
        if not self.main_window.image_files:
            QMessageBox.warning(self.main_window, "警告", "没有图片可以保存")
            return False
            
        if not output_folder:
            # 如果没有指定输出文件夹，弹出选择对话框
            output_folder = QFileDialog.getExistingDirectory(
                self.main_window,
                "选择保存文件夹"
            )
            
        if output_folder:
            success_count = 0
            for image_path in self.main_window.image_files:
                # 生成输出文件名
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(output_folder, f"{base_name}_watermarked.jpg")
                
                # 应用水印并保存
                if self.main_window.watermark_handler.apply_watermark_to_image(image_path, output_path):
                    success_count += 1
            
            self.main_window.status_label.setText(
                f"批量保存完成: {success_count}/{len(self.main_window.image_files)} 张图片"
            )
            return success_count > 0
        
        return False
    
    def get_image_info(self, file_path):
        """获取图片信息"""
        return ImageProcessor.get_image_info(file_path)
    
    def is_image_loaded(self, file_path):
        """检查图片是否已加载"""
        return file_path in self.main_window.image_files
    
    def get_loaded_images_count(self):
        """获取已加载图片数量"""
        return len(self.main_window.image_files)
    
    def clear_all_images(self):
        """清空所有图片"""
        self.main_window.image_list.clear()
        self.main_window.image_files.clear()
        self.main_window.current_image = None
        self.main_window.preview_area.clear()
        self.main_window.status_label.setText("已清空所有图片")
    
    def export_current_image(self):
        """导出当前图片（带水印）- 使用自定义对话框"""
        if not self.main_window.current_image:
            QMessageBox.warning(self.main_window, "警告", "请先选择一张图片")
            return False
            
        # 创建并显示导出对话框
        dialog = ExportDialog(self.main_window, self.main_window.current_image)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 获取用户设置
            settings = dialog.get_export_settings()
            
            # 获取原图片信息
            original_path = self.main_window.current_image
            original_name = os.path.basename(original_path)
            name_without_ext = os.path.splitext(original_name)[0]
            
            # 根据命名规则生成输出文件名
            if settings['naming_rule'] == 0:  # 保留原文件名
                output_name = f"{name_without_ext}.{settings['format']}"
            elif settings['naming_rule'] == 1:  # 添加前缀
                output_name = f"{settings['prefix']}{name_without_ext}.{settings['format']}"
            elif settings['naming_rule'] == 2:  # 添加后缀
                output_name = f"{name_without_ext}{settings['suffix']}.{settings['format']}"
            else:
                output_name = f"{name_without_ext}_watermarked.{settings['format']}"
                
            output_path = os.path.join(settings['output_folder'], output_name)
            
            # 如果文件已存在，询问是否覆盖
            if os.path.exists(output_path):
                reply = QMessageBox.question(
                    self.main_window,
                    "文件已存在",
                    f"文件 '{output_name}' 已存在。\n是否覆盖？",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return False
            
            # 应用水印并保存
            try:
                success = self.main_window.watermark_handler.apply_watermark_to_image(
                    original_path, 
                    output_path,
                    settings
                )
                
                if success:
                    # 统一路径分隔符为反斜杠
                    display_path = output_path.replace('/', '\\')
                    self.main_window.status_label.setText(f"图片已导出到: {display_path}")
                    QMessageBox.information(
                        self.main_window,
                        "导出成功",
                        f"图片已成功导出到:\n{display_path}"
                    )
                    return True
                else:
                    QMessageBox.critical(self.main_window, "错误", "导出图片失败")
                    return False
                    
            except Exception as e:
                QMessageBox.critical(self.main_window, "错误", f"导出图片时发生错误: {str(e)}")
                return False
        
        return False
    
    def export_all_images(self, output_folder=None, naming_rule="suffix", custom_text="_watermarked"):
        """批量导出所有图片（带水印）
        
        Args:
            output_folder: 输出文件夹路径
            naming_rule: 命名规则 ("original", "prefix", "suffix")
            custom_text: 自定义前缀或后缀文本
        """
        if not self.main_window.image_files:
            QMessageBox.warning(self.main_window, "警告", "没有图片可以导出")
            return False
            
        # 如果没有指定输出文件夹，弹出选择对话框
        if not output_folder:
            output_folder = QFileDialog.getExistingDirectory(
                self.main_window,
                "选择导出文件夹"
            )
            
        if not output_folder:
            return False
            
        # 检查是否有图片在原文件夹中
        original_dirs = set()
        for image_path in self.main_window.image_files:
            original_dirs.add(os.path.dirname(image_path))
            
        if any(os.path.normpath(output_folder) == os.path.normpath(orig_dir) 
               for orig_dir in original_dirs):
            reply = QMessageBox.question(
                self.main_window,
                "确认导出",
                "导出文件夹包含部分原图片所在的文件夹，这可能会覆盖原文件。\n是否继续？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return False
        
        success_count = 0
        failed_files = []
        
        for image_path in self.main_window.image_files:
            # 获取原图片信息
            original_name = os.path.basename(image_path)
            name_without_ext = os.path.splitext(original_name)[0]
            original_ext = os.path.splitext(original_name)[1]
            
            # 根据命名规则生成输出文件名
            if naming_rule == "original":
                output_name = original_name
            elif naming_rule == "prefix":
                output_name = f"{custom_text}{original_name}"
            elif naming_rule == "suffix":
                output_name = f"{name_without_ext}{custom_text}{original_ext}"
            else:
                output_name = f"{name_without_ext}_watermarked{original_ext}"
                
            output_path = os.path.join(output_folder, output_name)
            
            # 应用水印并保存
            if self.main_window.watermark_handler.apply_watermark_to_image(image_path, output_path):
                success_count += 1
            else:
                failed_files.append(original_name)
        
        # 显示结果
        if failed_files:
            failed_list = "\n".join(failed_files[:5])  # 最多显示5个失败文件
            if len(failed_files) > 5:
                failed_list += f"\n... 还有 {len(failed_files) - 5} 个文件"
            QMessageBox.warning(
                self.main_window,
                "导出完成（部分失败）",
                f"成功导出: {success_count}/{len(self.main_window.image_files)} 张图片\n\n失败的文件:\n{failed_list}"
            )
        else:
            QMessageBox.information(
                self.main_window,
                "导出完成",
                f"成功导出 {success_count} 张图片到:\n{output_folder}"
            )
        
        self.main_window.status_label.setText(
            f"批量导出完成: {success_count}/{len(self.main_window.image_files)} 张图片"
        )
        
        return success_count > 0