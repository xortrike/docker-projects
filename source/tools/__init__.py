"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

from terminal.system import System
from terminal.status import TerminalStatus
from tools.magento import MagentoTerminal
from tools.mysql import MySQLTerminal
from tools.xdebug import XdebugTerminal
from tools.elasticsearch import ElasticSearchTerminal
from tools.redis import RedisTerminal

class Tools(System):
    def __init__(self, project, containers):
        self.containers = containers
        self.config = project["tools"] if "tools" in project else {}

    def getTools(self):
        tools = ["magento", "xdebug", "mysql", "elasticsearch", "redis"]
        return list(filter(lambda name: name in self.config, tools))

    def run(self, name:str, user:str = None):
        if not name in self.config:
            self.error("There is no \"{0}\" property in your tools configurations.".format(name))
            return TerminalStatus.stop

        if name == "magento":
            config = self.config["magento"].copy()
            config["user"] = user if user else "root"
            MagentoTerminal(config, self.containers).loop()
        elif name == "xdebug":
            config = self.config["xdebug"].copy()
            XdebugTerminal(config, self.containers).loop()
        elif name == "mysql":
            config = self.config["mysql"].copy()
            MySQLTerminal(config, self.containers).loop()
        elif name == "elasticsearch":
            config = self.config["elasticsearch"].copy()
            ElasticSearchTerminal(config, self.containers).loop()
        elif name == "redis":
            config = self.config["redis"].copy()
            RedisTerminal(config, self.containers).loop()

        return TerminalStatus.abort
