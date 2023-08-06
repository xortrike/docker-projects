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
from tools    import Tools
from language import Language

class DockerContainers(Terminal):
    def __init__(self, project):
        super().__init__("{0} - Containers".format(project["name"]))
        self.inputTabCompleter = self.inputCompleter
        self.project = project
        self.containers = self.getContainers()
        self.mainMenu = self.getMenu()
        self.tools = Tools(self.project, self.containers)

    def inputCompleter(self, text, state):
        completions = []
        for word in self.tools.getTools():
            if word.startswith(text):
                completions.append(word)
        return completions[state]

    def getMenu(self):
        menu = []
        for i in range(0, len(self.containers)):
            menu.append(TerminalMenu(i + 1, self.containers[i]))
        return menu

    def getContainers(self):
        output = self.system.subprocess('docker container ls --format "{{.Names}}"')
        return list(filter(None, output.split("\n")))

    def displayDocumentation(self):
        super().displayDocumentation([
            Language.get("documentation_commands"),
            "[\033[33mmagento       \033[0m] - Open Magento 2 CLI",
            "[\033[33mmysql         \033[0m] - Open MySQL tools",
            "[\033[33mxdebug        \033[0m] - Open Xdebug tools",
            "[\033[33melasticsearch \033[0m] - Open ElasticSearch tools",
            "[\033[33mredis         \033[0m] - Open Redis tools",
            "",
            Language.get("documentation_params"),
            "[\033[33m--user, --u\033[0m] - Open container as another user (default user: root)."
        ])

    def runCommand(self, command):
        main = super().runCommand(command)
        if main != TerminalStatus.skip:
            return main

        commandValue = command.getCommand()
        paramUserName = command.getParam("user").value or command.getParam("u").value

        if commandValue.isnumeric():
            currentMenu = self.getMenuByIndex(self.mainMenu, int(commandValue))
            paramUserName = paramUserName if paramUserName else "root"
            self.system.cmd('docker exec -it --user {0} {1} /bin/bash'.format(paramUserName, currentMenu.title))
        elif commandValue in self.tools.getTools():
            return self.tools.run(commandValue, paramUserName)
        return TerminalStatus.skip
