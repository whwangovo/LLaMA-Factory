# app.py
# 主应用入口文件

import sys
import os

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 从前端导入UI启动函数
from frontend.ui import launch_ui

def main():
    """
    主函数，启动应用程序
    """
    launch_ui()

if __name__ == "__main__":
    main()