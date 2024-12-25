# Insight

Error Insight for Learning

## 快速开始

### 1. 创建并激活虚拟环境

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. 安装依赖项

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python insight.py
```

### 4. 关闭虚拟环境

```bash
deactivate
```

### 5. 构建应用程序

```bash
pyinstaller --onefile --windowed --icon=icon.ico insight.py
```

构建完成后，`dist`目录下会出现一个可执行文件。
