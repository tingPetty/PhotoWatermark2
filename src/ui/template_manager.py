"""
水印模板管理器
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class TemplateManager:
    """水印模板管理器"""
    
    def __init__(self, templates_file: str = "watermark_templates.json"):
        self.templates_file = templates_file
        self.last_settings_file = "last_watermark_settings.json"
    
    def save_template(self, name: str, template_data: Dict[str, Any]) -> bool:
        """
        保存模板
        
        Args:
            name: 模板名称
            template_data: 模板数据
            
        Returns:
            bool: 保存是否成功
        """
        try:
            templates = self.load_all_templates()
            
            # 添加元数据
            template_data['name'] = name
            template_data['created_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            template_data['updated_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            templates[name] = template_data
            
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(templates, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"保存模板失败: {e}")
            return False
    
    def load_template(self, name: str) -> Optional[Dict[str, Any]]:
        """
        加载指定模板
        
        Args:
            name: 模板名称
            
        Returns:
            Dict[str, Any] or None: 模板数据
        """
        try:
            templates = self.load_all_templates()
            return templates.get(name)
            
        except Exception as e:
            print(f"加载模板失败: {e}")
            return None
    
    def load_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        加载所有模板
        
        Returns:
            Dict[str, Dict[str, Any]]: 所有模板数据
        """
        if not os.path.exists(self.templates_file):
            return {}
        
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"加载模板列表失败: {e}")
            return {}
    
    def delete_template(self, name: str) -> bool:
        """
        删除模板
        
        Args:
            name: 模板名称
            
        Returns:
            bool: 删除是否成功
        """
        try:
            templates = self.load_all_templates()
            
            if name in templates:
                del templates[name]
                
                with open(self.templates_file, 'w', encoding='utf-8') as f:
                    json.dump(templates, f, ensure_ascii=False, indent=2)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"删除模板失败: {e}")
            return False
    
    def rename_template(self, old_name: str, new_name: str) -> bool:
        """
        重命名模板
        
        Args:
            old_name: 旧名称
            new_name: 新名称
            
        Returns:
            bool: 重命名是否成功
        """
        try:
            templates = self.load_all_templates()
            
            if old_name in templates:
                template_data = templates[old_name]
                template_data['name'] = new_name
                template_data['updated_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                templates[new_name] = template_data
                del templates[old_name]
                
                with open(self.templates_file, 'w', encoding='utf-8') as f:
                    json.dump(templates, f, ensure_ascii=False, indent=2)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"重命名模板失败: {e}")
            return False
    
    def template_exists(self, name: str) -> bool:
        """
        检查模板是否存在
        
        Args:
            name: 模板名称
            
        Returns:
            bool: 模板是否存在
        """
        templates = self.load_all_templates()
        return name in templates
    
    def get_template_count(self) -> int:
        """
        获取模板数量
        
        Returns:
            int: 模板数量
        """
        templates = self.load_all_templates()
        return len(templates)
    
    def save_last_settings(self, settings: Dict[str, Any]) -> bool:
        """
        保存最后一次的设置
        
        Args:
            settings: 设置数据
            
        Returns:
            bool: 保存是否成功
        """
        try:
            settings['saved_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.last_settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"保存最后设置失败: {e}")
            return False
    
    def load_last_settings(self) -> Optional[Dict[str, Any]]:
        """
        加载最后一次的设置
        
        Returns:
            Dict[str, Any] or None: 设置数据
        """
        if not os.path.exists(self.last_settings_file):
            return None
        
        try:
            with open(self.last_settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"加载最后设置失败: {e}")
            return None
    
    def export_templates(self, export_file: str) -> bool:
        """
        导出所有模板到文件
        
        Args:
            export_file: 导出文件路径
            
        Returns:
            bool: 导出是否成功
        """
        try:
            templates = self.load_all_templates()
            
            export_data = {
                'export_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'template_count': len(templates),
                'templates': templates
            }
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"导出模板失败: {e}")
            return False
    
    def import_templates(self, import_file: str, overwrite: bool = False) -> bool:
        """
        从文件导入模板
        
        Args:
            import_file: 导入文件路径
            overwrite: 是否覆盖现有模板
            
        Returns:
            bool: 导入是否成功
        """
        try:
            if not os.path.exists(import_file):
                return False
            
            with open(import_file, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # 检查文件格式
            if 'templates' not in import_data:
                return False
            
            current_templates = self.load_all_templates()
            imported_templates = import_data['templates']
            
            # 合并模板
            for name, template_data in imported_templates.items():
                if name not in current_templates or overwrite:
                    template_data['imported_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    current_templates[name] = template_data
            
            # 保存合并后的模板
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(current_templates, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"导入模板失败: {e}")
            return False
    
    def get_template_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        获取模板信息
        
        Args:
            name: 模板名称
            
        Returns:
            Dict[str, Any] or None: 模板信息
        """
        template = self.load_template(name)
        if not template:
            return None
        
        info = {
            'name': template.get('name', name),
            'created_time': template.get('created_time', '未知'),
            'updated_time': template.get('updated_time', '未知'),
            'has_text_watermark': bool(template.get('watermark_text', '')),
            'has_image_watermark': template.get('enable_image_watermark', False),
            'watermark_position': template.get('watermark_position', '未知'),
            'font_family': template.get('font_family', '未知'),
            'font_size': template.get('font_size', 0),
            'opacity': template.get('watermark_opacity', 0),
            'rotation': template.get('watermark_rotation', 0)
        }
        
        return info
    
    def create_default_template(self) -> Dict[str, Any]:
        """
        创建默认模板
        
        Returns:
            Dict[str, Any]: 默认模板数据
        """
        return {
            'name': '默认模板',
            'watermark_text': '水印文本',
            'font_family': 'Arial',
            'font_size': 24,
            'font_bold': False,
            'font_italic': False,
            'font_color': '#000000',
            'watermark_opacity': 80,
            'watermark_rotation': 0,
            'watermark_position': 'bottom_right',
            'watermark_x': 0,
            'watermark_y': 0,
            'enable_image_watermark': False,
            'image_watermark_path': '',
            'image_opacity': 80,
            'proportional_scale': True,
            'image_width': 100,
            'image_height': 100,
            'created_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def cleanup_old_files(self, days: int = 30) -> bool:
        """
        清理旧文件（可选功能）
        
        Args:
            days: 保留天数
            
        Returns:
            bool: 清理是否成功
        """
        try:
            # 这里可以实现清理逻辑，比如删除超过指定天数的备份文件等
            # 目前只是一个占位符
            return True
            
        except Exception as e:
            print(f"清理文件失败: {e}")
            return False