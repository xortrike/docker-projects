"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import requests
from terminal import Terminal
from terminal.status import TerminalStatus
from terminal.menu import TerminalMenu

class ElasticSearchTerminal(Terminal):
    def __init__(self, config, containers):
        super().__init__("ElasticSearch - Tools", "48;5;28m")
        self.config = config
        self.containers = containers
        self.verification()
        self.mainMenu = self.getMenu()

    def getMenu(self):
        return [
            TerminalMenu(1, "Get Indexs"),
            TerminalMenu(2, "Delete All")
        ]

    def runCommand(self, command):
        superResult = super().runCommand(command)
        if superResult != TerminalStatus.skip:
            return superResult

        commandValue = command.getCommand()
        if commandValue == "1":
            return self.ElasticSearch_Indexs()
        elif commandValue == "2":
            return self.ElasticSearch_Delete()
        return TerminalStatus.skip

    def verification(self):
        if "container" not in self.config:
            raise Exception("Configurations do not have a \"container\" property.")
        if self.config["container"] not in self.containers:
            raise Exception("The \"{0}\" container is not in the list of containers.".format(self.config["container"]))

    def ElasticSearch_Indexs(self):
        result = requests.get("http://localhost:9200/_cat/indices?v")
        print(result.text)
        return TerminalStatus.stop

    def ElasticSearch_Delete(self):
        result = requests.delete("http://localhost:9200/_all")
        print(result.text)
        return TerminalStatus.stop
