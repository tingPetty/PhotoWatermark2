"""
水印模板管理对话框
"""

import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QLineEdit, QMessageBox,
    QInputDialog, QFrame, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class TemplateDialog(QDialog):
    """模板管理对话框"""
    
    template_loaded = pyqtSignal(dict)  # 模板加载信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.templates_file = "watermark_templates.json"
        self.init_ui()
        self.load_templates()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("水印模板管理")
        self.setFixedSize(600, 450)
        self.setModal(True)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("水印模板管理")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding: 10px 0;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 分隔器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：模板列表
        left_widget = self._create_template_list()
        splitter.addWidget(left_widget)
        
        # 右侧：模板详情
        right_widget = self._create_template_details()
        splitter.addWidget(right_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)
        
        # 底部按钮
        button_layout = self._create_buttons()
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def _create_template_list(self):
        """创建模板列表区域"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout()
        
        # 列表标题
        list_title = QLabel("已保存的模板")
        list_title.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #555;
                padding: 5px;
            }
        """)
        layout.addWidget(list_title)
        
        # 模板列表
        self.template_list = QListWidget()
        self.template_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
                selection-background-color: #e3f2fd;
                outline: none;
                show-decoration-selected: 0;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
                border: none;
                outline: none;
                margin: 0px;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
                border: none;
                outline: none;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                border: none;
                outline: none;
            }
            QListWidget::item:focus {
                border: none;
                outline: none;
                background-color: #e3f2fd;
            }
        """)
        # 禁用焦点指示器
        self.template_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.template_list.currentItemChanged.connect(self.on_template_selected)
        layout.addWidget(self.template_list)
        
        # 列表操作按钮
        list_button_layout = QHBoxLayout()
        
        self.delete_btn = QPushButton("删除")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 15px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_template)
        list_button_layout.addWidget(self.delete_btn)
        
        self.rename_btn = QPushButton("重命名")
        self.rename_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 15px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        self.rename_btn.setEnabled(False)
        self.rename_btn.clicked.connect(self.rename_template)
        list_button_layout.addWidget(self.rename_btn)
        
        list_button_layout.addStretch()
        layout.addLayout(list_button_layout)
        
        widget.setLayout(layout)
        return widget
    
    def _create_template_details(self):
        """创建模板详情区域"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout()
        
        # 详情标题
        details_title = QLabel("模板详情")
        details_title.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #555;
                padding: 5px;
            }
        """)
        layout.addWidget(details_title)
        
        # 详情显示区域
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: #f9f9f9;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.details_text)
        
        widget.setLayout(layout)
        return widget
    
    def _create_buttons(self):
        """创建底部按钮"""
        button_layout = QHBoxLayout()
        
        button_layout.addStretch()
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        return button_layout
    
    def load_templates(self):
        """加载模板列表"""
        self.template_list.clear()
        
        if not os.path.exists(self.templates_file):
            return
        
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                templates = json.load(f)
            
            for template_name, template_data in templates.items():
                item = QListWidgetItem(template_name)
                item.setData(Qt.ItemDataRole.UserRole, template_data)
                self.template_list.addItem(item)
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载模板失败：{str(e)}")
    
    def on_template_selected(self, current, previous):
        """模板选择事件"""
        if current is None:
            self.details_text.clear()
            self.delete_btn.setEnabled(False)
            self.rename_btn.setEnabled(False)
            return
        
        # 启用按钮
        self.delete_btn.setEnabled(True)
        self.rename_btn.setEnabled(True)
        
        # 显示模板详情
        template_data = current.data(Qt.ItemDataRole.UserRole)
        if template_data:
            details = self._format_template_details(template_data)
            self.details_text.setPlainText(details)
    
    def _format_template_details(self, template_data):
        """格式化模板详情显示"""
        details = []
        details.append(f"模板名称: {template_data.get('name', '未知')}")
        details.append(f"创建时间: {template_data.get('created_time', '未知')}")
        details.append("")
        details.append("=== 文本水印设置 ===")
        details.append(f"水印文本: {template_data.get('watermark_text', '')}")
        details.append(f"字体: {template_data.get('font_family', '')}")
        details.append(f"字体大小: {template_data.get('font_size', 0)}")
        details.append(f"粗体: {'是' if template_data.get('font_bold', False) else '否'}")
        details.append(f"斜体: {'是' if template_data.get('font_italic', False) else '否'}")
        details.append(f"颜色: {template_data.get('font_color', '')}")
        details.append(f"阴影: {'是' if template_data.get('font_shadow', False) else '否'}")
        details.append(f"描边: {'是' if template_data.get('font_stroke', False) else '否'}")
        details.append(f"描边颜色: {template_data.get('stroke_color', '#ffffff')}")
        details.append(f"透明度: {template_data.get('watermark_opacity', 0)}%")
        details.append(f"旋转角度: {template_data.get('watermark_rotation', 0)}°")
        details.append("")
        details.append("=== 位置设置 ===")
        details.append(f"水印位置: {template_data.get('watermark_position', '')}")
        details.append(f"X偏移: {template_data.get('watermark_x', 0)}")
        details.append(f"Y偏移: {template_data.get('watermark_y', 0)}")
        details.append("")
        details.append("=== 图片水印设置 ===")
        details.append(f"启用图片水印: {'是' if template_data.get('enable_image_watermark', False) else '否'}")
        if template_data.get('enable_image_watermark', False):
            details.append(f"图片路径: {template_data.get('image_watermark_path', '')}")
            details.append(f"图片透明度: {template_data.get('image_opacity', 0)}%")
            details.append(f"保持比例: {'是' if template_data.get('proportional_scale', False) else '否'}")
            details.append(f"图片宽度: {template_data.get('image_width', 0)}px")
            details.append(f"图片高度: {template_data.get('image_height', 0)}px")
        
        return "\n".join(details)
    
    def save_current_template(self):
        """保存当前设置为模板"""
        if not self.parent_window:
            QMessageBox.warning(self, "错误", "无法获取当前设置")
            return
        
        # 获取模板名称
        name, ok = QInputDialog.getText(self, "保存模板", "请输入模板名称:")
        if not ok or not name.strip():
            return
        
        name = name.strip()
        
        # 收集当前设置
        template_data = self._collect_current_settings()
        template_data['name'] = name
        template_data['created_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存模板
        self._save_template(name, template_data)
        
        # 刷新列表
        self.load_templates()
        
        QMessageBox.information(self, "成功", f"模板 '{name}' 保存成功！")
    
    def _collect_current_settings(self):
        """收集当前的水印设置"""
        if not self.parent_window:
            return {}
        
        settings = {}
        
        # 文本水印设置
        settings['watermark_text'] = getattr(self.parent_window, 'watermark_text', '')
        
        # 字体设置
        if hasattr(self.parent_window, 'font_combo'):
            settings['font_family'] = self.parent_window.font_combo.currentFont().family()
        else:
            settings['font_family'] = 'Arial'
            
        if hasattr(self.parent_window, 'font_size_spin'):
            settings['font_size'] = self.parent_window.font_size_spin.value()
        else:
            settings['font_size'] = 24
            
        if hasattr(self.parent_window, 'bold_checkbox'):
            settings['font_bold'] = self.parent_window.bold_checkbox.isChecked()
        else:
            settings['font_bold'] = False
            
        if hasattr(self.parent_window, 'italic_checkbox'):
            settings['font_italic'] = self.parent_window.italic_checkbox.isChecked()
        else:
            settings['font_italic'] = False
            
        # 修复：从text_color属性获取颜色值
        if hasattr(self.parent_window, 'text_color'):
            settings['font_color'] = self.parent_window.text_color.name()
        else:
            settings['font_color'] = '#000000'
            
        # 阴影设置
        if hasattr(self.parent_window, 'shadow_checkbox'):
            settings['font_shadow'] = self.parent_window.shadow_checkbox.isChecked()
        else:
            settings['font_shadow'] = False
            
        # 描边设置
        if hasattr(self.parent_window, 'stroke_checkbox'):
            settings['font_stroke'] = self.parent_window.stroke_checkbox.isChecked()
        else:
            settings['font_stroke'] = False
            
        # 描边颜色设置
        if hasattr(self.parent_window, 'stroke_color'):
            settings['stroke_color'] = self.parent_window.stroke_color.name()
        else:
            settings['stroke_color'] = '#ffffff'
        
        # 透明度设置
        if hasattr(self.parent_window, 'opacity_slider'):
            settings['watermark_opacity'] = self.parent_window.opacity_slider.value()
        else:
            settings['watermark_opacity'] = 80
            
        # 旋转设置
        if hasattr(self.parent_window, 'rotation_slider'):
            settings['watermark_rotation'] = self.parent_window.rotation_slider.value()
        else:
            settings['watermark_rotation'] = 0
        
        # 位置设置
        watermark_position = getattr(self.parent_window, 'watermark_position', 'bottom_right')
        if hasattr(watermark_position, 'x') and hasattr(watermark_position, 'y'):
            # 如果是QPoint对象，转换为列表格式
            settings['watermark_position'] = [watermark_position.x(), watermark_position.y()]
        else:
            # 如果是字符串或其他格式，直接使用
            settings['watermark_position'] = watermark_position
        settings['watermark_x'] = getattr(self.parent_window, 'watermark_x', 0)
        settings['watermark_y'] = getattr(self.parent_window, 'watermark_y', 0)
        
        # 图片水印设置
        if hasattr(self.parent_window, 'enable_image_watermark'):
            settings['enable_image_watermark'] = self.parent_window.enable_image_watermark.isChecked()
            if hasattr(self.parent_window, 'image_watermark_path'):
                settings['image_watermark_path'] = getattr(self.parent_window, 'image_watermark_path', '')
            if hasattr(self.parent_window, 'image_opacity_slider'):
                settings['image_opacity'] = self.parent_window.image_opacity_slider.value()
            if hasattr(self.parent_window, 'proportional_scale'):
                settings['proportional_scale'] = self.parent_window.proportional_scale.isChecked()
            if hasattr(self.parent_window, 'image_width_spin'):
                settings['image_width'] = self.parent_window.image_width_spin.value()
            if hasattr(self.parent_window, 'image_height_spin'):
                settings['image_height'] = self.parent_window.image_height_spin.value()
        
        return settings
    
    def _save_template(self, name, template_data):
        """保存模板到文件"""
        templates = {}
        
        # 加载现有模板
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
            except:
                pass
        
        # 添加新模板
        templates[name] = template_data
        
        # 保存到文件
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(templates, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存模板失败：{str(e)}")
    
    def load_selected_template(self):
        """加载选中的模板"""
        current_item = self.template_list.currentItem()
        if not current_item:
            return
        
        template_data = current_item.data(Qt.ItemDataRole.UserRole)
        if template_data:
            self.template_loaded.emit(template_data)
            QMessageBox.information(self, "成功", f"模板 '{current_item.text()}' 加载成功！")
            self.close()
    
    def delete_template(self):
        """删除选中的模板"""
        current_item = self.template_list.currentItem()
        if not current_item:
            return
        
        template_name = current_item.text()
        
        # 确认删除
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除模板 '{template_name}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # 从文件中删除
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
                
                if template_name in templates:
                    del templates[template_name]
                    
                    with open(self.templates_file, 'w', encoding='utf-8') as f:
                        json.dump(templates, f, ensure_ascii=False, indent=2)
                    
                    # 刷新列表
                    self.load_templates()
                    QMessageBox.information(self, "成功", f"模板 '{template_name}' 删除成功！")
                    
            except Exception as e:
                QMessageBox.warning(self, "错误", f"删除模板失败：{str(e)}")
    
    def rename_template(self):
        """重命名选中的模板"""
        current_item = self.template_list.currentItem()
        if not current_item:
            return
        
        old_name = current_item.text()
        
        # 获取新名称
        new_name, ok = QInputDialog.getText(self, "重命名模板", "请输入新的模板名称:", text=old_name)
        if not ok or not new_name.strip() or new_name.strip() == old_name:
            return
        
        new_name = new_name.strip()
        
        # 更新文件
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
                
                if old_name in templates:
                    template_data = templates[old_name]
                    template_data['name'] = new_name
                    templates[new_name] = template_data
                    del templates[old_name]
                    
                    with open(self.templates_file, 'w', encoding='utf-8') as f:
                        json.dump(templates, f, ensure_ascii=False, indent=2)
                    
                    # 刷新列表
                    self.load_templates()
                    QMessageBox.information(self, "成功", f"模板重命名成功！")
                    
            except Exception as e:
                QMessageBox.warning(self, "错误", f"重命名模板失败：{str(e)}")


class SaveTemplateDialog(QDialog):
    """保存模板对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.templates_file = "watermark_templates.json"
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("保存水印模板")
        self.setFixedSize(400, 200)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("保存当前水印设置为模板")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
                padding: 10px 0;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 模板名称输入
        name_layout = QHBoxLayout()
        name_label = QLabel("模板名称:")
        name_label.setFixedWidth(80)
        name_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("请输入模板名称")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 5px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #2196f3;
            }
        """)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        layout.addStretch()
        
        # 按钮
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("保存")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_template)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_template(self):
        """保存模板"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "错误", "请输入模板名称")
            return
        
        # 收集当前设置
        template_data = self._collect_current_settings()
        template_data['name'] = name
        template_data['created_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存模板
        self._save_template(name, template_data)
        
        QMessageBox.information(self, "成功", f"模板 '{name}' 保存成功！")
        self.accept()
    
    def _collect_current_settings(self):
        """收集当前的水印设置"""
        if not self.parent_window:
            return {}
        
        settings = {}
        
        # 文本水印设置
        settings['watermark_text'] = getattr(self.parent_window, 'watermark_text', '')
        
        # 字体设置
        if hasattr(self.parent_window, 'font_combo'):
            settings['font_family'] = self.parent_window.font_combo.currentFont().family()
        else:
            settings['font_family'] = 'Arial'
            
        if hasattr(self.parent_window, 'font_size_spin'):
            settings['font_size'] = self.parent_window.font_size_spin.value()
        else:
            settings['font_size'] = 24
            
        if hasattr(self.parent_window, 'bold_checkbox'):
            settings['font_bold'] = self.parent_window.bold_checkbox.isChecked()
        else:
            settings['font_bold'] = False
            
        if hasattr(self.parent_window, 'italic_checkbox'):
            settings['font_italic'] = self.parent_window.italic_checkbox.isChecked()
        else:
            settings['font_italic'] = False
            
        # 修复：从text_color属性获取颜色值
        if hasattr(self.parent_window, 'text_color'):
            settings['font_color'] = self.parent_window.text_color.name()
        else:
            settings['font_color'] = '#000000'
            
        # 阴影设置
        if hasattr(self.parent_window, 'shadow_checkbox'):
            settings['font_shadow'] = self.parent_window.shadow_checkbox.isChecked()
        else:
            settings['font_shadow'] = False
            
        # 描边设置
        if hasattr(self.parent_window, 'stroke_checkbox'):
            settings['font_stroke'] = self.parent_window.stroke_checkbox.isChecked()
        else:
            settings['font_stroke'] = False
            
        # 描边颜色设置
        if hasattr(self.parent_window, 'stroke_color'):
            settings['stroke_color'] = self.parent_window.stroke_color.name()
        else:
            settings['stroke_color'] = '#ffffff'
        
        # 透明度设置
        if hasattr(self.parent_window, 'opacity_slider'):
            settings['watermark_opacity'] = self.parent_window.opacity_slider.value()
        else:
            settings['watermark_opacity'] = 80
            
        # 旋转设置
        if hasattr(self.parent_window, 'rotation_slider'):
            settings['watermark_rotation'] = self.parent_window.rotation_slider.value()
        else:
            settings['watermark_rotation'] = 0
        
        # 位置设置
        watermark_position = getattr(self.parent_window, 'watermark_position', 'bottom_right')
        if hasattr(watermark_position, 'x') and hasattr(watermark_position, 'y'):
            # 如果是QPoint对象，转换为列表格式
            settings['watermark_position'] = [watermark_position.x(), watermark_position.y()]
        else:
            # 如果是字符串或其他格式，直接使用
            settings['watermark_position'] = watermark_position
        settings['watermark_x'] = getattr(self.parent_window, 'watermark_x', 0)
        settings['watermark_y'] = getattr(self.parent_window, 'watermark_y', 0)
        
        # 图片水印设置
        if hasattr(self.parent_window, 'enable_image_watermark'):
            settings['enable_image_watermark'] = self.parent_window.enable_image_watermark.isChecked()
            if hasattr(self.parent_window, 'image_watermark_path'):
                settings['image_watermark_path'] = getattr(self.parent_window, 'image_watermark_path', '')
            if hasattr(self.parent_window, 'image_opacity_slider'):
                settings['image_opacity'] = self.parent_window.image_opacity_slider.value()
            if hasattr(self.parent_window, 'proportional_scale'):
                settings['proportional_scale'] = self.parent_window.proportional_scale.isChecked()
            if hasattr(self.parent_window, 'image_width_spin'):
                settings['image_width'] = self.parent_window.image_width_spin.value()
            if hasattr(self.parent_window, 'image_height_spin'):
                settings['image_height'] = self.parent_window.image_height_spin.value()
            # 处理图片水印位置
            if hasattr(self.parent_window, 'image_watermark_position'):
                image_position = getattr(self.parent_window, 'image_watermark_position', None)
                if image_position and hasattr(image_position, 'x') and hasattr(image_position, 'y'):
                    settings['image_watermark_position'] = [image_position.x(), image_position.y()]
                elif image_position:
                    settings['image_watermark_position'] = image_position
        
        return settings
    
    def _save_template(self, name, template_data):
        """保存模板到文件"""
        templates = {}
        
        # 加载现有模板
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
            except:
                pass
        
        # 添加新模板
        templates[name] = template_data
        
        # 保存到文件
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(templates, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存模板失败：{str(e)}")


class LoadTemplateDialog(QDialog):
    """加载模板对话框"""
    
    template_selected = pyqtSignal(dict)  # 模板选择信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.templates_file = "watermark_templates.json"
        self.init_ui()
        self.load_templates()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("加载水印模板")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("选择要加载的水印模板")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
                padding: 10px 0;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 模板列表
        self.template_list = QListWidget()
        self.template_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
                selection-background-color: #e3f2fd;
                outline: none;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
                border: none;
                outline: none;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                border: none;
                outline: none;
            }
            QListWidget::item:focus {
                border: none;
                outline: none;
                background-color: #e3f2fd;
            }
        """)
        # 禁用焦点指示器
        self.template_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.template_list.itemDoubleClicked.connect(self.load_template)
        layout.addWidget(self.template_list)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        load_btn = QPushButton("加载")
        load_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        load_btn.clicked.connect(self.load_template)
        button_layout.addWidget(load_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_templates(self):
        """加载模板列表"""
        self.template_list.clear()
        
        if not os.path.exists(self.templates_file):
            item = QListWidgetItem("暂无保存的模板")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.template_list.addItem(item)
            return
        
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                templates = json.load(f)
            
            if not templates:
                item = QListWidgetItem("暂无保存的模板")
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                self.template_list.addItem(item)
                return
            
            for template_name, template_data in templates.items():
                item = QListWidgetItem(f"{template_name} ({template_data.get('created_time', '未知时间')})")
                item.setData(Qt.ItemDataRole.UserRole, template_data)
                self.template_list.addItem(item)
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载模板失败：{str(e)}")
    
    def load_template(self):
        """加载选中的模板"""
        current_item = self.template_list.currentItem()
        if not current_item or not current_item.data(Qt.ItemDataRole.UserRole):
            return
        
        template_data = current_item.data(Qt.ItemDataRole.UserRole)
        self.template_selected.emit(template_data)
        self.accept()