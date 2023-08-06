"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import enum

class TerminalStatus(enum.Enum):
    abort = 1
    stop = 2
    skip = 3
    next = 4
    notify = 5
