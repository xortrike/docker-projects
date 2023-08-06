"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

class TerminalSubmenu:
    def __init__(self, index:int, title:str, data:dict = {}):
        self._index = index
        self._title = title
        self._data = data

    @property
    def index(self) -> int:
        return self._index

    @property
    def title(self) -> str:
        return self._title

    @property
    def data(self) -> dict:
        return self._data
