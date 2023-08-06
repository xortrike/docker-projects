"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import os
import subprocess
from terminal import Terminal
from terminal.status import TerminalStatus
from terminal.menu import TerminalMenu

class XdebugTerminal(Terminal):
    def __init__(self, config, containers):
        super().__init__("Xdebug - Tools", "48;5;28m")
        self.config = config
        self.containers = containers
        self.verification()
        self.mainMenu = self.getMenu()

    def getMenu(self):
        return [
            TerminalMenu(1, "Status"),
            TerminalMenu(2, "Enable"),
            TerminalMenu(3, "Disable")
        ]

    def runCommand(self, command):
        superResult = super().runCommand(command)
        if superResult != TerminalStatus.skip:
            return superResult

        commandValue = command.getCommand()
        if commandValue == "1":
            return self.Xdebug_Status()
        elif commandValue == "2":
            return self.Xdebug_Enable()
        elif commandValue == "3":
            return self.Xdebug_Disable()
        return TerminalStatus.skip

    def verification(self):
        if "container" not in self.config:
            raise Exception("Configurations do not have a \"container\" property.")
        if self.config["container"] not in self.containers:
            raise Exception("The \"{0}\" container is not in the list of containers.".format(self.config["container"]))
        if not self.isExist():
            raise Exception("Xdebug module not found.")

    def isExist(self):
        container = self.config["container"]
        checkFile = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini"
        output = subprocess.getoutput("docker exec {0} bash -c \"if [ -f {1} ] || [ -f {1}.bak ]; then echo 1; else echo 0; fi\"".format(container, checkFile))
        return True if int(output) else False

    def Xdebug_Status(self):
        container = self.config["container"]
        checkFile = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini"
        output = subprocess.getoutput("docker exec {0} bash -c \"if [ -f {1} ]; then echo 1; else echo 0; fi\"".format(container, checkFile))
        print("\033[92mXdebug is enabled.\033[39m" if int(output) else "\033[91mXdebug is disabled.\033[39m")
        return TerminalStatus.stop

    def Xdebug_Enable(self):
        container = self.config["container"]
        moveFrom = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini.bak"
        moveTo = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini"
        os.system("docker exec {0} bash -c \"if [ -f {1} ]; then mv {1} {2}; fi\"".format(container, moveFrom, moveTo))
        os.system("docker restart {0}".format(container))
        self.Xdebug_Status()
        return TerminalStatus.stop

    def Xdebug_Disable(self):
        container = self.config["container"]
        moveFrom = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini"
        moveTo = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini.bak"
        os.system("docker exec {0} bash -c \"if [ -f {1} ]; then mv {1} {2}; fi\"".format(container, moveFrom, moveTo))
        os.system("docker restart {0}".format(container))
        self.Xdebug_Status()
        return TerminalStatus.stop
