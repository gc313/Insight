import streamlit.web.cli as stcli
import os
import sys
import logging

def get_root_path():
    # 获取当前脚本的根路径
    if getattr(sys, 'frozen', False):  # 如果是 PyInstaller 打包的环境
        return sys._MEIPASS  # 获取临时目录路径
    return os.path.dirname(__file__)  # 普通运行环境

def setup_logging():
    # 设置日志配置
    log_dir = os.path.join(get_root_path(), 'log')
    os.makedirs(log_dir, exist_ok=True)  # 确保日志文件夹存在

    log_file_path = os.path.join(log_dir, 'runtime.log')

    logging.basicConfig(
        filename=log_file_path,
        filemode='a',  # 追加模式
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    

script_path = os.path.join(get_root_path(), "app.py")

def resolve_path(path):
    #解析相对路径为绝对路径
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path

if __name__ == "__main__":
    setup_logging()  # 初始化日志设置

    # 检查 app.py 是否存在
    if not os.path.exists(script_path):
        logging.error(f"代码路径 '{script_path}' 不存在!")
        sys.exit(1)

    # 构造 Streamlit 命令
    sys.argv = [
        "streamlit",
        "run",
        script_path,  # 替换为解析后的路径
        "--global.developmentMode=false",
    ]

    try:
        logging.info("启动 Streamlit 应用")
        sys.exit(stcli.main())
    except Exception as e:
        logging.error(f"启动 Streamlit 出错: {e}")
        sys.exit(1)