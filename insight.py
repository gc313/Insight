# Copyright (C) 2024  ThisWaySir

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Additionally, we encourage all users to review the full license agreement to fully understand their rights and obligations. For more information about the GNU General Public License, please visit:
# - Chinese: [GNU Official Website - GNU GPLv3 Chinese](https://www.gnu.org/licenses/quick-guide-gplv3.zh-cn.html)
# - English: [GNU Official Website - GNU GPLv3 English](https://www.gnu.org/licenses/gpl-3.0.en.html)

# Thank you for supporting the open source community and the free software movement!

import threading
import subprocess
import time
import os
import sys
from pathlib import Path
import requests
import webbrowser
import atexit
import signal
import psutil

streamlit_process = None

def start_streamlit():
    global streamlit_process
    # 启动 Streamlit 应用，并绑定到所有网络接口
    if getattr(sys, 'frozen', False):
        streamlit_script = os.path.join(sys._MEIPASS, "app.py")
        streamlit_process = subprocess.Popen(
            ["streamlit", "run", streamlit_script, "--server.address=0.0.0.0"],
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # 仅适用于 Windows
        )
    else:
        streamlit_process = subprocess.Popen(
            ["streamlit", "run", "app.py", "--server.address=0.0.0.0"],
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # 仅适用于 Windows
        )

def stop_streamlit():
    global streamlit_process
    if streamlit_process:
        try:
            # 发送终止信号给 Streamlit 进程
            streamlit_process.terminate()
            streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # 如果进程未在 5 秒内终止，则强制终止
            streamlit_process.kill()

def ensure_streamlit_config():
    config_path = Path.home() / ".streamlit" / "config.toml"
    config_dir = config_path.parent

    # 确保目录存在
    config_dir.mkdir(parents=True, exist_ok=True)

    # 如果配置文件不存在，则创建它
    if not config_path.exists():
        with open(config_path, 'w') as f:
            f.write("[server]\n")
            f.write("headless = true\n")
            f.write("port = 8501\n")
            f.write("enableCORS = true\n")  # 保留默认设置
            f.write("enableXsrfProtection = true\n")  # 保留默认设置
            f.write("address = '0.0.0.0'\n")
            f.write("\n")  # 添加空行分隔不同部分
            f.write("[browser]\n")
            f.write("gatherUsageStats = false\n")  # 正确的配置选项

def check_server_ready(url="http://localhost:8501", timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                print("Streamlit 服务器已准备好！")
                return True
        except requests.exceptions.RequestException as e:
            print(f"检查服务器状态时发生错误: {e}")
        time.sleep(0.5)  # 等待0.5秒再重试
    print("Streamlit 服务器启动超时。")
    return False

def kill_port(port):
    terminated_pids = set()  # 记录已终止的进程ID
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            connections = proc.net_connections(kind='inet')
            for conn in connections:
                if conn.laddr and conn.laddr.port == port and proc.pid not in terminated_pids:
                    print(f"终止进程 {proc.pid} ({proc.name()}) 占用端口 {port}")
                    proc.kill()
                    terminated_pids.add(proc.pid)  # 添加到已终止集合
                    break  # 终止后跳出内层循环
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# 注册退出处理函数，确保在程序结束时终止 Streamlit 进程
atexit.register(stop_streamlit)

# 捕获 Ctrl+C 并调用 stop_streamlit
signal.signal(signal.SIGINT, lambda signum, frame: stop_streamlit())

if __name__ == "__main__":
    # 确保 Streamlit 配置文件存在
    ensure_streamlit_config()

    # 杀死占用端口 8501 的进程
    kill_port(8501)

    # 在后台线程中启动 Streamlit 应用
    thread = threading.Thread(target=start_streamlit)
    thread.daemon = True
    thread.start()

    # 动态检查 Streamlit 服务器是否已准备好
    if check_server_ready():
        # 使用系统默认浏览器打开 Streamlit 应用
        webbrowser.open("http://localhost:8501")
    else:
        print("Streamlit 服务器启动已超时。")