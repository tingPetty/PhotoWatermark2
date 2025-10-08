#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
启动脚本 - 运行PhotoWatermark2应用程序
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入主程序入口
from main import main

if __name__ == "__main__":
    main()