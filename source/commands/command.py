"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

from commands.params import Params
from commands.param import Param

class Command:
    def __init__(self, commandString: str):
        index = commandString.find(" ")
        self._command = commandString if index < 0 else commandString[0:index]
        self._params = Params() if index < 0 else Params(commandString[index + 1:])

    def __str__(self):
        return "Command({0})".format(self._command)

    def getCommand(self) -> str:
        point = self._command.find(".")
        return self._command[0:point] if point > 0 and self._command[0:point].isnumeric() else self._command

    def getSubcommand(self) -> str:
        point = self._command.find(".") + 1
        return self._command[point:] if point > 0 and self._command[point:].isnumeric() else ""

    def getParams(self) -> Params:
        return self._params

    def getParam(self, key = 1) -> Param:
        return self._params.getParam(key)
