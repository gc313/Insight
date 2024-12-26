import streamlit.web.cli as stcli
import sys
import logging
from pathlib import Path

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

def check_and_run_streamlit(development_mode=False):
    """检查并启动 Streamlit 应用"""
    script_name = "app.py"

    # 构造 Streamlit 命令
    sys.argv = [
        "streamlit",
        "run",
        str(Path(get_root_path(), script_name)),  # 使用 get_root_path 获取正确的路径
        "--global.developmentMode=false" if not development_mode else "--global.developmentMode=true",
        #"--server.headless=true",  # 启用无头模式
        "--browser.gatherUsageStats=false"  # 禁用遥测数据收集
    ]

    try:
        logging.info(f"启动 Streamlit 应用, 命令行参数: {sys.argv}")
        stcli.main()
    except Exception as e:
        logging.error(f"启动 Streamlit 出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_logging()  # 初始化日志设置

    # 启动 Streamlit 应用
    check_and_run_streamlit()