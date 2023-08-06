"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

class Param:
    def __init__(self, paramString:str = ""):
        self._original = paramString
        if paramString.startswith("--"):
            paramString = paramString[2:]
        index = paramString.find("=")
        self._key = paramString.strip() if index < 0 else paramString[0:index].strip()
        self._value = paramString[index + 1:].strip() if index > 0 else ""

    def __str__(self):
        return "Param({0})".format(self._original)

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> str:
        return self._value

    @property
    def original(self) -> str:
        return self._original
