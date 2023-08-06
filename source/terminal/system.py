"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import os
import subprocess
import readline

class System:
    def pause(self):
        input("\nPress [Enter] key to continue...")

    def clear(self):
        os.system("clear")

    def input(self, text, completer = None):
        if completer:
            readline.parse_and_bind("tab: complete")
            readline.set_completer(completer)
        else:
            readline.parse_and_bind('tab: self-insert')
        return input(text)

    def subprocess(self, text):
        return subprocess.getoutput(text)

    def cmd(self, text):
        os.system(text)

    def header(self, title, color):
        print("\033[{0}            \033[1m\033[97m{1}\x1B[K\033[0m".format(color, title))

    def print(self, message):
        print(message)

    def error(self, message):
        print("\033[1;31mError: {0}\033[0m".format(message))

    def warning(self, message):
        print("\033[38;5;208mWarning: {0}\033[0m".format(message))
