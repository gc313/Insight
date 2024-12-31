import streamlit.web.cli as stcli
import sys
import os
import logging
from pathlib import Path
from core.constants import app_config as ac

def get_root_path():
    """获取根路径"""
    if getattr(sys, 'frozen', False):  # 如果是 PyInstaller 打包的环境
        # print("Running in a PyInstaller bundle")
        return Path(sys._MEIPASS)  # 获取临时目录路径
    else:
        # print("Running in a normal Python environment")
        return Path(__file__).parent  # 获取脚本所在目录

def setup_logging(log_dir='log'):
    """设置日志配置"""
    log_dir = Path.cwd() / log_dir  # 日志保存在当前工作目录
    log_dir.mkdir(exist_ok=True, parents=True)  # 确保日志文件夹存在

    log_file_path = log_dir / 'runtime.log'
    # print(f"Logging to: {log_file_path}")

    logging.basicConfig(
        filename=log_file_path,
        filemode='a',  # 追加模式
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )
    logging.info(f"日志系统已初始化，日志文件路径: {log_file_path}")
    
# 生成配置文件
def ensure_streamlit_config():
    # 确保目录存在
    config_dir = ac.CONFIG_DIR_PATH
    os.makedirs(config_dir, exist_ok=True)
    
    # 创建 credentials.toml 文件占位，避免询问电子邮件地址
    credentials_file_path = ac.CREDENTIALS_FILE_PATH
    if not os.path.exists(credentials_file_path):
        with open(credentials_file_path, 'w') as credentials_file:
            credentials_file.write(ac.CREDENTIALS_CONTENT)
    
    # 创建 config.toml 文件
    config_file_path = ac.CONFIG_FILE_PATH
    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as config_file:
            config_file.write(ac.CONFIG_CONTENT)

def check_and_run_streamlit():
    """检查并启动 Streamlit 应用"""
    script_name = "app.py"

    # 构造 Streamlit 命令
    sys.argv = [
        "streamlit",
        "run",
        str(Path(get_root_path(), script_name)) # 使用 get_root_path 获取正确的路径
    ]

    try:
        logging.info(f"启动 Streamlit 应用, 命令行参数: {sys.argv}")
        stcli.main()
    except Exception as e:
        logging.error(f"启动 Streamlit 出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    
    ensure_streamlit_config() # 确保配置文件存在
    setup_logging() # 初始化日志设置
    check_and_run_streamlit() #启动 Streamlit 应用