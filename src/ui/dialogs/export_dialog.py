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
    QFileDialog, QMessageBox, QCheckBox, QSlider,
    QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt


class ExportDialog(QDialog):
    """导出设置对话框"""
    
    def __init__(self, parent=None, current_image_path=None):
        super().__init__(parent)
        self.current_image_path = current_image_path
        self.selected_folder = None
        
        # 获取原始图片信息
        self.original_width = 0
        self.original_height = 0
        if current_image_path and os.path.exists(current_image_path):
            from core.image_processor import ImageProcessor
            image_info = ImageProcessor.get_image_info(current_image_path)
            if image_info:
                self.original_width = image_info['width']
                self.original_height = image_info['height']
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        self.setWindowTitle("导出图片设置")
        self.setFixedSize(600, 550)
        self.setModal(True)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 格式选择组
        format_group = self._create_format_group()
        main_layout.addWidget(format_group)
        
        # 质量设置组
        quality_group = self._create_quality_group()
        main_layout.addWidget(quality_group)
        
        # 尺寸调整组
        size_group = self._create_size_group()
        main_layout.addWidget(size_group)
        
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
        self.format_combo.currentTextChanged.connect(self._on_format_changed)
        
        layout.addWidget(QLabel("格式:"))
        layout.addWidget(self.format_combo)
        layout.addStretch()
        
        return group

    def _create_quality_group(self):
        """创建质量设置组"""
        group = QGroupBox("图片质量")
        layout = QVBoxLayout(group)
        
        # 质量滑块（仅对JPEG有效）
        quality_layout = QHBoxLayout()
        
        self.quality_label = QLabel("JPEG质量:")
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(95)
        self.quality_slider.valueChanged.connect(self._on_quality_changed)
        
        self.quality_value_label = QLabel("95%")
        self.quality_value_label.setMinimumWidth(40)
        
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_value_label)
        
        layout.addLayout(quality_layout)
        
        # 质量说明
        quality_info = QLabel("提示：质量越高文件越大，质量越低压缩率越高")
        quality_info.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(quality_info)
        
        return group

    def _create_size_group(self):
        """创建尺寸调整组"""
        group = QGroupBox("图片尺寸")
        layout = QVBoxLayout(group)
        
        # 原始尺寸显示
        if self.original_width > 0 and self.original_height > 0:
            original_info = QLabel(f"原始尺寸: {self.original_width} × {self.original_height} 像素")
            original_info.setStyleSheet("color: #666; font-size: 11px;")
            layout.addWidget(original_info)
        
        # 尺寸调整选项
        self.size_group_buttons = QButtonGroup()
        
        # 保持原始尺寸
        self.keep_original_radio = QRadioButton("保持原始尺寸")
        self.keep_original_radio.setChecked(True)
        self.size_group_buttons.addButton(self.keep_original_radio, 0)
        layout.addWidget(self.keep_original_radio)
        
        # 按百分比缩放
        percent_layout = QHBoxLayout()
        self.percent_radio = QRadioButton("按百分比缩放:")
        self.percent_spin = QSpinBox()
        self.percent_spin.setRange(1, 500)
        self.percent_spin.setValue(100)
        self.percent_spin.setSuffix("%")
        self.percent_spin.setEnabled(False)
        
        self.size_group_buttons.addButton(self.percent_radio, 1)
        percent_layout.addWidget(self.percent_radio)
        percent_layout.addWidget(self.percent_spin)
        percent_layout.addStretch()
        layout.addLayout(percent_layout)
        
        # 自定义尺寸
        self.custom_radio = QRadioButton("自定义尺寸:")
        self.size_group_buttons.addButton(self.custom_radio, 2)
        layout.addWidget(self.custom_radio)
        
        # 自定义尺寸的详细设置
        custom_details_layout = QGridLayout()
        custom_details_layout.setContentsMargins(20, 0, 0, 0)  # 左边缩进20像素
        
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(self.original_width if self.original_width > 0 else 800)
        self.width_spin.setEnabled(False)
        
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(self.original_height if self.original_height > 0 else 600)
        self.height_spin.setEnabled(False)
        
        self.keep_aspect_ratio = QCheckBox("保持宽高比")
        self.keep_aspect_ratio.setChecked(True)
        self.keep_aspect_ratio.setEnabled(False)
        
        custom_details_layout.addWidget(QLabel("宽度:"), 0, 0)
        custom_details_layout.addWidget(self.width_spin, 0, 1)
        custom_details_layout.addWidget(QLabel("像素"), 0, 2)
        custom_details_layout.addWidget(QLabel("高度:"), 1, 0)
        custom_details_layout.addWidget(self.height_spin, 1, 1)
        custom_details_layout.addWidget(QLabel("像素"), 1, 2)
        custom_details_layout.addWidget(self.keep_aspect_ratio, 2, 0, 1, 3)
        
        layout.addLayout(custom_details_layout)
        
        # 连接信号
        self.percent_radio.toggled.connect(lambda checked: self.percent_spin.setEnabled(checked))
        self.custom_radio.toggled.connect(self._on_custom_size_toggled)
        self.width_spin.valueChanged.connect(self._on_width_changed)
        self.height_spin.valueChanged.connect(self._on_height_changed)
        
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

    def _on_format_changed(self, format_text):
        """格式变化事件处理"""
        # 根据格式启用/禁用质量设置
        is_jpeg = format_text.upper() == "JPEG"
        self.quality_label.setEnabled(is_jpeg)
        self.quality_slider.setEnabled(is_jpeg)
        self.quality_value_label.setEnabled(is_jpeg)

    def _on_quality_changed(self, value):
        """质量滑块变化事件处理"""
        self.quality_value_label.setText(f"{value}%")

    def _on_custom_size_toggled(self, checked):
        """自定义尺寸选项切换事件处理"""
        self.width_spin.setEnabled(checked)
        self.height_spin.setEnabled(checked)
        self.keep_aspect_ratio.setEnabled(checked)

    def _on_width_changed(self, width):
        """宽度变化事件处理"""
        if (self.keep_aspect_ratio.isChecked() and 
            self.keep_aspect_ratio.isEnabled() and 
            self.original_width > 0 and self.original_height > 0):
            # 根据宽度按比例调整高度
            ratio = self.original_height / self.original_width
            new_height = int(width * ratio)
            self.height_spin.blockSignals(True)
            self.height_spin.setValue(new_height)
            self.height_spin.blockSignals(False)

    def _on_height_changed(self, height):
        """高度变化事件处理"""
        if (self.keep_aspect_ratio.isChecked() and 
            self.keep_aspect_ratio.isEnabled() and 
            self.original_width > 0 and self.original_height > 0):
            # 根据高度按比例调整宽度
            ratio = self.original_width / self.original_height
            new_width = int(height * ratio)
            self.width_spin.blockSignals(True)
            self.width_spin.setValue(new_width)
            self.width_spin.blockSignals(False)

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
            'suffix': self.suffix_edit.text().strip() if self.suffix_radio.isChecked() else "",
            'quality': self.quality_slider.value(),
            'size_mode': self.size_group_buttons.checkedId(),
            'percent_scale': self.percent_spin.value(),
            'custom_width': self.width_spin.value(),
            'custom_height': self.height_spin.value(),
            'keep_aspect_ratio': self.keep_aspect_ratio.isChecked()
        }
        return settings