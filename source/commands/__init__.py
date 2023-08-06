"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

from commands.command import Command

class Commands:
    def __init__(self, inputString):
        self._i = 0
        self._commands = []
        if inputString:
            for commandString in inputString.strip().split(";"):
                if commandString:
                    self._commands.append(Command(commandString.strip()))

    def __str__(self):
        return "Commands({0})".format(self.total)

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i < self.total:
            self._i += 1
            return self._commands[self._i - 1]
        else:
            raise StopIteration

    @property
    def total(self):
        return len(self._commands)

    def getCommands(self):
        return self._commands

    def getCommand(self, index = 1):
        if type(index) == str and index.isnumeric():
            index = int(index)
        if type(index) == int and (index > 0 and index <= self.total):
            return self._commands[index - 1]
        return None
