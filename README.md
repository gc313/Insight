# <img src="/pic/insight.png" alt="Insight Logo" style="width:64px;height:64px;margin-right:10px;"> Insight

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

## 构建应用程序

### 1. 第一次打包

如果使用虚拟环境，需要先进入虚拟环境，这里假设虚拟环境名为`venv`。

```bash
pyinstaller --onefile --windowed --additional-hooks-dir=./hooks --icon=icon.ico insight.py --clean
```

此时在根目录的`dist`目录下会出现一个可执行文件，可以删除不要。

### 2. 编辑.spec文件

根目录下会出现`insight.spec`文件，打开后修改如下：

```python
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# 假设虚拟环境为venv
datas = [
    # 将虚拟环境中 Streamlit 的 runtime 文件夹打包到目标路径 "./streamlit/runtime"
    ("./venv/Lib/site-packages/streamlit/runtime", "./streamlit/runtime"),
    
    # 将当前目录下的 app.py 文件打包到目标路径的根目录 "./"
    ("./app.py", "./"),
    
    # 将 src 文件夹及其内容打包到目标路径 "./src"
    ("./src", "./src"),
    
    # 将 pic 文件夹及其内容打包到目标路径 "./pic"
    ("./pic", "./pic")
]

# 收集 Streamlit 包中的所有数据文件，并将其添加到 datas 列表中
datas += collect_data_files('streamlit')

# 复制 Streamlit 包的元数据（如依赖关系等），并将其添加到 datas 列表中
datas += copy_metadata('streamlit')

a = Analysis(
    ['insight.py'],
    pathex=[],
    binaries=[],
    datas=datas,  # 添加之前定义的 datas 列表
    hiddenimports=[],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='insight',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True, # 目前还是推荐设置为True，否则在设置界面输入内容时会有黑框闪烁
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
```

### 3. 再次打包

```bash
pyinstaller insight.spec --clean
```

打包完成后获取根目录的`dist`目录下的可执行文件即可。
