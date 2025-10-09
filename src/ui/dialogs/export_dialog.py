#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
导出对话框模块
提供自定义导出选项的对话框
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, 
    QRadioButton, QButtonGroup, QGroupBox,
    QFileDialog, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt


class ExportDialog(QDialog):
    """导出设置对话框"""
    
    def __init__(self, parent=None, current_image_path=None):
        super().__init__(parent)
        self.current_image_path = current_image_path
        self.selected_folder = None
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        self.setWindowTitle("导出图片设置")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 格式选择组
        format_group = self._create_format_group()
        main_layout.addWidget(format_group)
        
        # 输出文件夹选择组
        folder_group = self._create_folder_group()
        main_layout.addWidget(folder_group)
        
        # 文件命名规则组
        naming_group = self._create_naming_group()
        main_layout.addWidget(naming_group)
        
        # 按钮区域
        button_layout = self._create_button_layout()
        main_layout.addLayout(button_layout)
        
    def _create_format_group(self):
        """创建格式选择组"""
        group = QGroupBox("输出格式")
        layout = QHBoxLayout(group)
        
        # 格式选择
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPEG", "PNG"])
        self.format_combo.setCurrentText("JPEG")
        
        layout.addWidget(QLabel("格式:"))
        layout.addWidget(self.format_combo)
        layout.addStretch()
        
        return group
        
    def _create_folder_group(self):
        """创建文件夹选择组"""
        group = QGroupBox("输出文件夹")
        layout = QVBoxLayout(group)
        
        # 文件夹选择区域
        folder_layout = QHBoxLayout()
        
        self.folder_edit = QLineEdit()
        self.folder_edit.setReadOnly(True)
        self.folder_edit.setPlaceholderText("请选择输出文件夹...")
        
        self.browse_button = QPushButton("浏览...")
        self.browse_button.clicked.connect(self._browse_folder)
        
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(self.browse_button)
        
        layout.addLayout(folder_layout)
        
        # 警告标签
        self.warning_label = QLabel()
        self.warning_label.setStyleSheet("color: red; font-size: 12px;")
        self.warning_label.hide()
        layout.addWidget(self.warning_label)
        
        return group
        
    def _create_naming_group(self):
        """创建文件命名规则组"""
        group = QGroupBox("文件命名规则")
        layout = QVBoxLayout(group)
        
        # 单选按钮组
        self.naming_group = QButtonGroup()
        
        # 保留原文件名
        self.original_radio = QRadioButton("保留原文件名")
        self.original_radio.setChecked(True)
        self.naming_group.addButton(self.original_radio, 0)
        layout.addWidget(self.original_radio)
        
        # 添加前缀
        prefix_layout = QHBoxLayout()
        self.prefix_radio = QRadioButton("添加前缀:")
        self.prefix_edit = QLineEdit("wm_")
        self.prefix_edit.setMaximumWidth(150)
        self.prefix_edit.setEnabled(False)
        # 设置样式，删除底下的横线
        self.prefix_edit.setStyleSheet("QLineEdit { border: 1px solid #ccc; background-color: white; }")
        
        self.naming_group.addButton(self.prefix_radio, 1)
        prefix_layout.addWidget(self.prefix_radio)
        prefix_layout.addWidget(self.prefix_edit)
        prefix_layout.addStretch()
        layout.addLayout(prefix_layout)
        
        # 添加后缀
        suffix_layout = QHBoxLayout()
        self.suffix_radio = QRadioButton("添加后缀:")
        self.suffix_edit = QLineEdit("_watermarked")
        self.suffix_edit.setMaximumWidth(150)
        self.suffix_edit.setEnabled(False)
        # 设置样式，删除底下的横线
        self.suffix_edit.setStyleSheet("QLineEdit { border: 1px solid #ccc; background-color: white; }")
        
        self.naming_group.addButton(self.suffix_radio, 2)
        suffix_layout.addWidget(self.suffix_radio)
        suffix_layout.addWidget(self.suffix_edit)
        suffix_layout.addStretch()
        layout.addLayout(suffix_layout)
        
        # 连接信号
        self.prefix_radio.toggled.connect(lambda checked: self.prefix_edit.setEnabled(checked))
        self.suffix_radio.toggled.connect(lambda checked: self.suffix_edit.setEnabled(checked))
        
        return group
        
    def _create_button_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        layout.addStretch()
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        # 确认导出按钮
        self.export_button = QPushButton("确认导出")
        self.export_button.clicked.connect(self._validate_and_accept)
        self.export_button.setDefault(True)
        
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.export_button)
        
        return layout
        
    def _browse_folder(self):
        """浏览文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "选择输出文件夹",
            os.path.expanduser("~")
        )
        
        if folder:
            self.selected_folder = folder
            # 统一使用反斜杠显示路径
            display_path = folder.replace('/', '\\')
            self.folder_edit.setText(display_path)
            self._check_folder_warning()
            
    def _check_folder_warning(self):
        """检查文件夹警告"""
        if self.current_image_path and self.selected_folder:
            current_dir = os.path.dirname(self.current_image_path)
            if os.path.normpath(self.selected_folder) == os.path.normpath(current_dir):
                self.warning_label.setText("⚠️ 警告: 选择的输出文件夹与原图片文件夹相同，可能会覆盖原图片！")
                self.warning_label.show()
            else:
                self.warning_label.hide()
        else:
            self.warning_label.hide()
            
    def _validate_and_accept(self):
        """验证设置并接受对话框"""
        if not self.selected_folder:
            QMessageBox.warning(self, "警告", "请选择输出文件夹！")
            return
            
        # 检查命名规则
        if self.prefix_radio.isChecked() and not self.prefix_edit.text().strip():
            QMessageBox.warning(self, "警告", "请输入前缀内容！")
            return
            
        if self.suffix_radio.isChecked() and not self.suffix_edit.text().strip():
            QMessageBox.warning(self, "警告", "请输入后缀内容！")
            return
            
        self.accept()
        
    def get_export_settings(self):
        """获取导出设置"""
        settings = {
            'format': self.format_combo.currentText().lower(),
            'output_folder': self.selected_folder,
            'naming_rule': self.naming_group.checkedId(),
            'prefix': self.prefix_edit.text().strip() if self.prefix_radio.isChecked() else "",
            'suffix': self.suffix_edit.text().strip() if self.suffix_radio.isChecked() else ""
        }
        return settings