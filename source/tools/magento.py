"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import re
from terminal import Terminal
from terminal.status import TerminalStatus
from terminal.menu import TerminalMenu
from terminal.submenu import TerminalSubmenu
from commands.command import Command

class MagentoTerminal(Terminal):
    def __init__(self, config, containers):
        super().__init__("Magento 2 - Terminal", "48;5;202m")
        self.config = config
        self.containers = containers
        self.verification()
        self.mainMenu = self.getMenu()

    def verification(self):
        if "container" not in self.config:
            raise Exception("Configurations do not have a \"container\" property.")
        if self.config["container"] not in self.containers:
            raise Exception("The \"{0}\" container is not in the list of containers.".format(self.config["container"]))

    def getMenu(self):
        menu = []

        commands = self.getCommands()
        if not commands or len(commands) == 0:
            raise Exception("An error occurred while reading commands.")

        for group in commands:
            if "hide_groups" in self.config and group["group"] in self.config["hide_groups"]:
                continue
            submenu = []
            strPad = max(list(map(lambda item: len(item["command"]), group["commands"]))) + 8
            for command in group["commands"]:
                submenuClass = TerminalSubmenu(
                    len(submenu) + 1,
                    "\033[32m{0}\033[0m{1}\033[0m".format(
                        command["command"].ljust(strPad),
                        command["description"]
                    ),
                    {"command": command["command"]}
                )
                submenu.append(submenuClass)
            menuClass = TerminalMenu(
                len(menu) + 1,
                "\033[33m{0}\033[0m".format(group["group"]),
                submenu
            )
            menu.append(menuClass)

        return menu

    def getCommands(self):
        print("\033[32mReading command list...\033[0m")
        lines = self.system.subprocess("docker exec --user {0} {1} php bin/magento list".format(
            self.config["user"],
            self.config["container"]
        )).split("\n")
        if lines[0].startswith("Magento CLI"):
            self.headerTitle = "{0} [{1}]".format(lines[0], self.config["user"])
        index = lines.index("Available commands:") + 3
        commands = []
        lastIndex = len(lines)
        while index < lastIndex:
            if lines[index].startswith("  "):
                commandAndDescription = lines[index][2:].split(re.search(r'\s{2,}', lines[index][2:]).group(0))
                commands[-1]["commands"].append({
                    "command": commandAndDescription[0],
                    "description": commandAndDescription[1]
                })
            elif lines[index].startswith(" "):
                commands.append({
                    "group": lines[index].strip(),
                    "commands": []
                })
            index += 1
        return commands

    def runCommand(self, command:Command):
        main = super().runCommand(command)
        if main != TerminalStatus.skip:
            return main

        selectedMenu = self.getSelectedMenu(command)
        if selectedMenu:
            self.system.cmd('docker exec -it --user {0} {1} php bin/magento {2} {3}'.format(
                self.config["user"],
                self.config["container"],
                selectedMenu.data["command"],
                command.getParams().original
            ))
            return TerminalStatus.next
        return TerminalStatus.skip
