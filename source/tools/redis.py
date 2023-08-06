"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

from terminal import Terminal
from terminal.status import TerminalStatus
from terminal.menu import TerminalMenu

class RedisTerminal(Terminal):
    def __init__(self, config, containers):
        super().__init__("Redis - Tools", "48;5;28m")
        self.config = config
        self.containers = containers
        self.verification()
        self.mainMenu = self.getMenu()

    def getMenu(self):
        return [
            TerminalMenu(1, "Flushall")
        ]

    def runCommand(self, command):
        superResult = super().runCommand(command)
        if superResult != TerminalStatus.skip:
            return superResult

        commandValue = command.getCommand()
        if commandValue == "1":
            return self.Redis_Flushall()
        return TerminalStatus.skip

    def verification(self):
        if "container" not in self.config:
            raise Exception("Configurations do not have a \"container\" property.")
        if self.config["container"] not in self.containers:
            raise Exception("The \"{0}\" container is not in the list of containers.".format(self.config["container"]))

    def Redis_Flushall(self):
        self.system.cmd("docker exec -it --user {0} {1} redis-cli flushall".format(
            self.config["user"],
            self.config["container"]
        ))
        return TerminalStatus.stop
