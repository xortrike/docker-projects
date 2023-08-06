"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import os
import json
from containers import DockerContainers
from terminal import Terminal
from terminal.status import TerminalStatus
from terminal.menu import TerminalMenu
from language import Language
from commands.command import Command

class DockerProjects(Terminal):

    def __init__(self):
        super().__init__(Language.get("projects_title"), "48;5;4m")
        self.mainMenu = self.getMenu()

    def getMenu(self):
        menu = []
        projects = self.getProjects()
        for i in range(0, len(projects)):
            name = projects[i]["name"]
            title = name if projects[i]["status"] else "\033[1;31m{0}\033[0m".format(name)
            menu.append(TerminalMenu(i + 1, title, [], projects[i]))
        return menu

    def getProjects(self):
        baseDir = os.path.dirname(os.path.abspath(__file__))
        if os.path.isfile(baseDir):
            baseDir = os.path.dirname(baseDir)
        projectsFile = os.path.join(baseDir, "projects.json")
        if os.path.exists(projectsFile) and os.path.isfile(projectsFile):
            strem = open(projectsFile)
            projects = json.load(strem)
            strem.close()
            for project in projects:
                if "name" not in project:
                    project["name"] = "???"
                project["status"] = "docker" in project and os.path.exists(
                    os.path.join(project["docker"], "docker-compose.yml")
                )
            return projects
        else:
            raise Exception(Language.get("projects_exception"))

    def displayDocumentation(self):
        super().displayDocumentation([
            Language.get("documentation_commands"),
            "[\033[33minfo, i\033[0m] - " + Language.get("projects_documentation_info"),
            "",
            Language.get("documentation_params"),
            "[\033[33m--stop,  --s\033[0m] - " + Language.get("projects_documentation_stop"),
            "[\033[33m--down,  --d\033[0m] - " + Language.get("projects_documentation_down"),
            "[\033[33m--build, --b\033[0m] - " + Language.get("projects_documentation_build")
        ])

    def runCommand(self, command: Command):
        main = super().runCommand(command)
        if main != TerminalStatus.skip:
            return main

        commandValue = command.getCommand()
        if commandValue in ["info", "i"]:
            self.displayInformation()
            return TerminalStatus.stop
        elif self.menuExists(commandValue):
            currentMenu = self.getMenuByIndex(self.mainMenu, int(commandValue))
            project = currentMenu.data
            if not project["status"]:
                self.system.error(Language.get("projects_command_exception").format(project["name"]))
                return TerminalStatus.stop
            if command.getParam('s').key or command.getParam('stop').key:
                self.stopProject(project)
                return TerminalStatus.abort
            elif command.getParam('d').key or command.getParam('down').key:
                self.downProject(project)
                return TerminalStatus.abort
            elif command.getParam('b').key or command.getParam('build').key:
                self.buildProject(project)
                return TerminalStatus.abort
            else:
                self.startProject(project)
                DockerContainers(project).loop()
                self.stopProject(project)
                return TerminalStatus.abort
        return TerminalStatus.skip

    def displayInformation(self):
        self.displayHeader(Language.get("projects_info_title"))
        print("{0} {1}".format(Language.get("projects_info_language"), Language.getRegionName()))
        print("{0} {1}".format(Language.get("projects_info_author"), "Xortrike"))
        print("{0} {1}".format(Language.get("projects_info_copyright"), "Copyright 2017 Xortrike"))
        print("{0} {1}".format(Language.get("projects_info_license"), "GNU General Public License v3.0"))
        print("{0} {1}".format(Language.get("projects_info_version"), "1.0.0"))
        print("{0} {1}".format(Language.get("projects_info_repository"), "https://github.com/xortrike/docker-projects"))

    def startProject(self, project):
        self.system.clear()
        print(Language.get("projects_command_start").format(project["name"]))
        cmd = 'docker-compose --compatibility --project-directory "{0}" --file "{0}/docker-compose.yml" up -d'
        self.system.cmd(cmd.format(project["docker"]))

    def stopProject(self, project):
        self.system.clear()
        print(Language.get("projects_command_stop").format(project["name"]))
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" stop'
        self.system.cmd(cmd.format(project["docker"]))

    def downProject(self, project):
        self.system.clear()
        print(Language.get("projects_command_down").format(project["name"]))
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" down'
        self.system.cmd(cmd.format(project["docker"]))

    def buildProject(self, project):
        self.system.clear()
        print(Language.get("projects_command_build").format(project["name"]))
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" build'
        self.system.cmd(cmd.format(project["docker"]))
