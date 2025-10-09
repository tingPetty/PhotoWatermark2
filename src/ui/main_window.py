#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口类模块
"""

import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QStatusBar, QMenuBar, QToolBar, QFileDialog,
    QListWidget, QListWidgetItem, QSplitter, QMessageBox
)
from PyQt6.QtCore import Qt, QSize, QMimeData
from PyQt6.QtGui import QAction, QIcon, QDragEnterEvent, QDropEvent, QPixmap

from core.image_processor import ImageProcessor


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口基本属性
        self.setWindowTitle("PhotoWatermark2 - 图片水印工具")
        self.resize(1000, 700)
        
        # 图片数据
        self.image_files = []  # 存储图片文件路径
        self.current_image = None  # 当前选中的图片
        
        # 初始化UI组件
        self._init_ui()
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        
        # 启用拖放功能
        self.setAcceptDrops(True)
        
    def _init_ui(self):
        """初始化UI布局"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧图片列表
        self.image_list = QListWidget()
        self.image_list.setMinimumWidth(200)
        self.image_list.itemClicked.connect(self._on_image_selected)
        splitter.addWidget(self.image_list)
        
        # 右侧区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 预览区域
        self.preview_area = QLabel("图片预览区域")
        self.preview_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_area.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ddd;")
        right_layout.addWidget(self.preview_area, 3)
        
        # 水印设置区域（占位）
        watermark_widget = QWidget()
        watermark_widget.setStyleSheet("background-color: #f8f8f8; border: 1px solid #ddd;")
        watermark_layout = QVBoxLayout(watermark_widget)
        watermark_layout.addWidget(QLabel("水印设置区域 (将在后续实现)"))
        right_layout.addWidget(watermark_widget, 1)
        
        splitter.addWidget(right_widget)
        
        # 设置分割器比例
        splitter.setSizes([200, 800])
        
        # 添加到主布局
        main_layout.addWidget(splitter)
        
    def _create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 打开图片动作
        open_action = QAction("打开图片", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_image)
        file_menu.addAction(open_action)
        
        # 保存图片动作
        save_action = QAction("保存图片", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        
        # 水印菜单
        watermark_menu = menu_bar.addMenu("水印")
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        
        # 关于动作
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)
        
    def _create_tool_bar(self):
        """创建工具栏"""
        tool_bar = QToolBar("主工具栏")
        tool_bar.setIconSize(QSize(16, 16))
        self.addToolBar(tool_bar)
        
        # 添加打开图片按钮
        open_action = QAction("打开图片", self)
        open_action.triggered.connect(self._open_image)
        tool_bar.addAction(open_action)
        
        # 添加保存图片按钮
        save_action = QAction("保存图片", self)
        tool_bar.addAction(save_action)
        
        tool_bar.addSeparator()
        
        # 添加水印按钮
        add_watermark_action = QAction("添加水印", self)
        tool_bar.addAction(add_watermark_action)
        
    def _create_status_bar(self):
        """创建状态栏"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # 添加状态信息
        self.status_label = QLabel("就绪")
        status_bar.addWidget(self.status_label)
        
    def _open_image(self):
        """打开图片对话框"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("图片文件 (*.jpg *.jpeg *.png *.bmp *.gif)")
        
        if file_dialog.exec():
            file_names = file_dialog.selectedFiles()
            self.status_label.setText(f"已选择 {len(file_names)} 个文件")
            self._load_images(file_names)
    
    def _load_images(self, file_paths):
        """加载图片文件"""
        for file_path in file_paths:
            # 检查文件是否已经在列表中
            if file_path in self.image_files:
                continue
                
            # 获取图片信息
            image_info = ImageProcessor.get_image_info(file_path)
            if not image_info:
                QMessageBox.warning(self, "警告", f"无法加载图片: {file_path}")
                continue
                
            # 添加到图片文件列表
            self.image_files.append(file_path)
            
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
            self.image_list.addItem(item)
        
        # 如果有图片，选择第一个
        if self.image_list.count() > 0 and not self.current_image:
            self.image_list.setCurrentRow(0)
            self._on_image_selected(self.image_list.item(0))
    
    def _on_image_selected(self, item):
        """图片选择事件处理"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.current_image = file_path
        
        # 加载图片并显示
        image = ImageProcessor.load_image(file_path)
        if image:
            pixmap = ImageProcessor.pil_to_pixmap(image)
            # 调整图片大小以适应预览区域
            scaled_pixmap = pixmap.scaled(
                self.preview_area.width(), 
                self.preview_area.height(),
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.preview_area.setPixmap(scaled_pixmap)
            
            # 更新状态栏
            image_info = ImageProcessor.get_image_info(file_path)
            self.status_label.setText(
                f"当前图片: {os.path.basename(file_path)} - "
                f"{image_info['width']}x{image_info['height']} - "
                f"{image_info['format']} - {image_info['size_kb']}KB"
            )
    
    # 拖放事件处理
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件处理"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """拖拽放下事件处理"""
        file_paths = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            # 检查是否是支持的图片格式
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                file_paths.append(file_path)
        
        if file_paths:
            self._load_images(file_paths)
            self.status_label.setText(f"已导入 {len(file_paths)} 个图片文件")