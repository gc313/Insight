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

import subprocess
import streamlit as st
from core.constants import app_config as ac

def get_latest_version():
    # try:
    #     # 执行 git describe --tags 命令来获取最新的 tag
    #     version = subprocess.check_output(['git', 'describe', '--tags'], stderr=subprocess.STDOUT).strip().decode('utf-8')
    # except subprocess.CalledProcessError:
    #     # 如果没有找到 tag，返回默认值
    #     version = "unknown"
    return ac.VERSION

def show_copy_right():
    copyright = "Copyright © 2024  ThisWaySir"
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; width: 100%;">
            <p style="font-size: 0.875em; color: #9e9e9e; margin: 0;">{copyright}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def about_info():
    app_name = ac.APP_NAME
    version = get_latest_version()
    st.markdown(f"""
## 关于 {app_name}

- **版本:** {version}

### 开源许可

{app_name} 遵循 GNU 通用公共许可证 (GNU General Public License, GPL) 版本 3.0 发布。这意味着您有权利自由使用、研究、分享（复制）和改进该软件。同时，我们也要求任何基于此软件创建的衍生作品同样遵循这一许可协议，以确保整个社区的利益得到保护。GPLv3还提供了额外的保护措施，防止数字版权管理（DRM）技术限制用户的自由。

您可以访问以下链接了解更多关于GPLv3的信息：

- 中文: [GNU 官方网站 - GNU GPLv3 中文](https://www.gnu.org/licenses/quick-guide-gplv3.zh-cn.html)
- 英文: [GNU 官方网站 - GNU GPLv3 English](https://www.gnu.org/licenses/gpl-3.0.en.html)

### GitHub 仓库

如果您有兴趣参与开发或想查看项目的最新进展，请访问我们的GitHub仓库:
[https://github.com/gc313/Insight](https://github.com/gc313/Insight)

感谢您选择并支持{app_name}！
""")
    show_copy_right()