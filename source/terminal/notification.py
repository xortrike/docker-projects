"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import os
from sys import platform

class Notification:
    def display(self, title, message):
        if platform == "linux":
            os.system('notify-send "{0}" "{1}"'.format(title, message))
