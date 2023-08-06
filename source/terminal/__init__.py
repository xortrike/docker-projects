"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import sys
import readline
import traceback
from language import Language
from commands import Commands
from commands.command import Command
from terminal.status import TerminalStatus
from terminal.menu import TerminalMenu
from terminal.submenu import TerminalSubmenu
from terminal.system import System
from terminal.notification import Notification

class Terminal:
    mainMenu = {}
    mainLoop = True
    openGroupByIndex = -1
    inputTabCompleter = None

    def __init__(self, title="Terminal", color="48;5;4m"):
        self.headerTitle = title
        self.headerColor = color
        self.system = System()
        self.notify = Notification()
        readline.clear_history()

    def loop(self):
        while self.mainLoop:
            self.displayMenu()
            try:
                self.runCommands(Commands(self.system.input("Commands: ", self.inputTabCompleter)))
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                f = open("exception.log", "w")
                f.write("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
                f.close()
                if exc_value:
                    self.system.error(exc_value)
                self.system.pause()
                self.mainLoop = False

    def displayHeader(self, title=None, color=None):
        self.system.header(title or self.headerTitle, color or self.headerColor)
        print("")

    def displayMenu(self):
        self.system.clear()
        self.displayHeader()
        for menu in self.mainMenu:
            if self.openGroupByIndex == menu.index:
                print("{0:3} - {1}".format(menu.index, menu.title))
                subPad = str(len(str(max(list(map(lambda item: item.index, menu.submenu))))))
                for submenu in menu.submenu:
                    print(("{0:3}.{1:"+subPad+"} - {2}").format(menu.index, submenu.index, submenu.title))
            else:
                print("{0:3} - {1}".format(menu.index, menu.title))
        print("")

    def displayDocumentation(self, rows = []):
        self.system.clear()
        self.displayHeader("Documentation")
        for row in rows:
            print(row)

    def runCommands(self, commands:Commands):
        self.system.clear()
        pause = True if commands.total > 0 else False
        try:
            for command in commands:
                status = self.runCommand(command)
                if status == TerminalStatus.abort:
                    pause = False
                    break
                elif status == TerminalStatus.stop:
                    pause = True
                    break
                elif status == TerminalStatus.skip:
                    pause = False
                elif status == TerminalStatus.next:
                    pause = True
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if exc_value:
                self.system.error(exc_value)
            pause = True
        if pause == True:
            self.system.pause()

    def runCommand(self, command:Command):
        commandValue = command.getCommand()
        if commandValue in ["x", "exit", "0"]:
            self.mainLoop = False
            return TerminalStatus.abort
        elif commandValue in ["h", "help"]:
            self.displayDocumentation()
            return TerminalStatus.stop
        elif commandValue in ["n", "notify"]:
            self.notify.display(self.headerTitle, Language.get("notification_message"))
            return TerminalStatus.notify
        elif commandValue and commandValue.isnumeric():
            currentMenu = self.getMenuByIndex(self.mainMenu, int(commandValue))
            if currentMenu and len(currentMenu.submenu) > 0:
                if not command.getSubcommand():
                    self.openGroupByIndex = -1 if self.openGroupByIndex == int(commandValue) else int(commandValue)
                    return TerminalStatus.abort
        return TerminalStatus.skip

    def menuExists(self, menuIndex:int, submenuIndex:int = None) -> bool:
        if type(menuIndex) == str and menuIndex.isnumeric():
            menuIndex = int(menuIndex)
        if type(submenuIndex) == str and submenuIndex.isnumeric():
            submenuIndex = int(submenuIndex)
        for item in self.mainMenu:
            if item.index == menuIndex:
                if submenuIndex:
                    for subitem in item.submenu:
                        if subitem.index == submenuIndex:
                            return True
                else:
                    return True
        return False

    def getMenuByIndex(self, menu:TerminalMenu or TerminalSubmenu, index:int) -> TerminalMenu or TerminalSubmenu or None:
        for item in menu:
            if item.index == index:
                return item
        return None

    def getSelectedMenu(self, command:Command) -> TerminalMenu or TerminalSubmenu or None:
        commandValue = command.getCommand()
        if commandValue.isnumeric():
            currentMenu = self.getMenuByIndex(self.mainMenu, int(commandValue))
            subcommandValue = command.getSubcommand()
            if currentMenu and subcommandValue.isnumeric():
                return self.getMenuByIndex(currentMenu.submenu, int(subcommandValue))
        return None
