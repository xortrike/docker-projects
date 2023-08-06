"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

from commands.param import Param

class Params:
    def __init__(self, paramsString:str = ""):
        self._original = paramsString
        self._i = 0
        self._params = []

        paramString = ""
        paramType = 0
        singleQuoteСlosed = True
        doubleQuoteСlosed = True

        for chr in paramsString:
            if chr == "-" and singleQuoteСlosed and doubleQuoteСlosed:
                if paramType == 2:
                    paramType = 1
                    self._params.append(Param(paramString.strip()))
                    paramString = ""
                else:
                    paramType += 1
                    continue

            if chr == "\"" and singleQuoteСlosed:
                doubleQuoteСlosed = not doubleQuoteСlosed
            elif chr == "\'" and doubleQuoteСlosed:
                singleQuoteСlosed = not singleQuoteСlosed

            if paramType == 2:
                paramString += chr

        if paramString:
            self._params.append(Param(paramString.strip()))

    def __str__(self):
        return "Params({0})".format(self.total)

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i < len(self._params):
            self._i += 1
            return self._params[self._i - 1]
        else:
            raise StopIteration

    @property
    def total(self):
        return len(self._params)

    @property
    def original(self) -> str:
        return self._original

    def getParam(self, key = 1):
        if type(key) == int or (type(key) == str and key.isnumeric()):
            index = int(key) - 1
            if index in range(0, self.total):
                return self._params[index]
        else:
            for param in self._params:
                if param.key == key:
                    return param
        return Param()
