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

import os

# 应用名称
APP_NAME = 'Insight'

# 版本
VERSION = 'v1.1.0'

# 路径
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
USER_DIR = os.path.expanduser('~')

# 颜色
PRIMARY_COLOR = '#6BAED6'
BACKGROUND_COLOR = '#FFFFFF'
SECONDARY_BACKGROUND_COLOR = '#F0F2F6'
TEXT_COLOR = '#31333F'

# 字体
PRIMARY_FONT = 'sans serif'


# 图标
PIC_DIR = 'pic'
LOGO_NAME = 'insight.png'
ICON_NAME = 'icon16.ico'

IMAGE_PATH = os.path.join(ROOT_DIR, PIC_DIR, ICON_NAME)
ICON_PATH = IMAGE_PATH

# 配置文件
CONFIG_DIR_NAME = '.streamlit'
CONFIG_FILE_NAME = 'config.toml'
CREDENTIALS_FILE_NAME = 'credentials.toml'
CONFIG_DIR_PATH = os.path.join(USER_DIR, CONFIG_DIR_NAME)
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, CONFIG_FILE_NAME)
CREDENTIALS_FILE_PATH = os.path.join(CONFIG_DIR_PATH, CREDENTIALS_FILE_NAME)

CONFIG_CONTENT = f"""
[browser]
gatherUsageStats = false

[theme]
primaryColor="{PRIMARY_COLOR}"
backgroundColor="{BACKGROUND_COLOR}"
secondaryBackgroundColor="{SECONDARY_BACKGROUND_COLOR}"
textColor="{TEXT_COLOR}"
font="{PRIMARY_FONT}"
"""

CREDENTIALS_CONTENT = f"""
[general]
email = ""
"""