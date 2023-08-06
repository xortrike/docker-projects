"""
@author     Xortrike
@copyright  Copyright 2017 Xortrike
@license    GNU General Public License v3.0
@version    1.0.0
@repository https://github.com/xortrike/docker-projects
"""

import os
from terminal import Terminal
from terminal.status import TerminalStatus
from terminal.menu import TerminalMenu
from terminal.submenu import TerminalSubmenu

class MySQLTerminal(Terminal):
    authorization = False
    databases = []
    sqlfiles = []

    def __init__(self, config, containers):
        super().__init__("MySQL - Tools", "48;5;28m")
        self.config = config
        self.containers = containers
        self.verification()
        self.mainMenu = self.getMenu()

    def getMenu(self):
        return [
            TerminalMenu(1, "Authorization" if self.authorization else "\033[91mAuthorization\033[0m", [
                TerminalSubmenu(1, "Login"),
                TerminalSubmenu(2, "Logout")
            ]),
            TerminalMenu(2, "Show databases"),
            TerminalMenu(3, "Create database"),
            TerminalMenu(4, "Import database"),
            TerminalMenu(5, "Export database"),
            TerminalMenu(6, "Drop database")
        ]

    def runCommand(self, command):
        superResult = super().runCommand(command)
        if superResult != TerminalStatus.skip:
            return superResult

        commandValue = command.getCommand()
        if commandValue == "1":
            subcommandValue = command.getSubcommand()
            if subcommandValue == "1":
                return self.MySQL_Login()
            elif subcommandValue == "2":
                return self.MySQL_Logout()
        elif commandValue == "2":
            return self.MySQL_Show()
        elif commandValue == "3":
            return self.MySQL_Create()
        elif commandValue == "4":
            return self.MySQL_Import()
        elif commandValue == "5":
            return self.MySQL_Export()
        elif commandValue == "6":
            return self.MySQL_Drop()

        return TerminalStatus.skip

    def displayDocumentation(self):
        super().displayDocumentation([
            "MySQL version: {0}".format(self.execute("SELECT VERSION()").split("\n")[1])
        ])

    def verification(self):
        if "container" not in self.config:
            raise Exception("Configurations do not have a \"container\" property.")
        if self.config["container"] not in self.containers:
            raise Exception("The \"{0}\" container is not in the list of containers.".format(self.config["container"]))
        if "user" not in self.config:
            raise Exception("In your configuration don't have a MySQL user name.")
        self.authorization = self.hasLoginPath()

    def hasLoginPath(self):
        execute = "docker exec -i {0} mysql_config_editor print --all".format(self.config["container"])
        output = self.system.subprocess(execute)
        return False if output.find("[client]") < 0 else True

    def hasAuthorize(self):
        if not self.authorization:
            print("To work with databases, you need to authorize.")
            self.system.pause()
            return False
        return True

    def MySQL_Login(self):
        print("\tLogin")
        container = self.config["container"]
        user = self.config["user"]
        print("Please, enter password for \"{0}\" user (MySQL connect).".format(user))
        self.system.cmd("docker exec -i {0} mysql_config_editor set --login-path=client --host=localhost --user={1} --password".format(container, user))

        self.authorization = self.hasLoginPath()
        if self.authorization:
            print("The authorization password has been saved.")
        else:
            self.system.error("Failed to logint")

        return TerminalStatus.stop

    def MySQL_Logout(self):
        print("\tLogout")
        container = self.config["container"]
        self.system.cmd("docker exec -i {0} mysql_config_editor remove --login-path=client".format(container))

        self.authorization = self.hasLoginPath()
        if self.authorization:
            self.system.error("Failed to logout")
        else:
            print("The authorization password has been deleted.")

        return TerminalStatus.stop

    def MySQL_Show(self):
        if not self.hasAuthorize():
            return TerminalStatus.abort

        dbList = self.getDatabases()
        print("Available databases:\n")
        for name in dbList:
            print(" - {0}".format(name))
        return TerminalStatus.stop

    def MySQL_Create(self):
        if not self.hasAuthorize():
            return TerminalStatus.abort

        print("Create database.\n")

        self.databases = self.getDatabases()

        dbName = self.system.input("Database name: ", self.Input_Database)

        if not dbName:
            return TerminalStatus.abort

        if dbName in self.databases:
            raise Exception("The \"{0}\" database already exists.".format(dbName))
        
        output = self.execute("CREATE DATABASE IF NOT EXISTS \`{0}\`;".format(dbName))
        if len(output) > 0:
            raise Exception(output)
        if "users" in self.config:
            for user in self.config["users"]:
                self.execute("GRANT ALL PRIVILEGES ON \`{0}\`.* TO '{1}'@'%';".format(dbName, user))
            self.execute("FLUSH PRIVILEGES;")

        self.databases = self.getDatabases()

        if dbName in self.databases:
            print("Database \"{0}\" was created.".format(dbName))
        else:
            self.system.error("Something went wrong. The database has not been created.")

        return TerminalStatus.stop

    def MySQL_Import(self):
        if not self.hasAuthorize():
            return TerminalStatus.abort

        print("Import database.\n")

        self.databases = self.getDatabases()
        self.sqlfiles = self.getListDir()

        dbName = self.system.input("Database name: ", self.Input_Database)
        fileName = self.system.input("Import from file: ", self.Input_File)
        
        if not dbName or not fileName:
            return TerminalStatus.abort

        if dbName not in self.databases:
            raise Exception("Database \"{0}\" does not exist, please create the database before importing.")

        container = self.config["container"]
        filePath = os.path.join(self.config["dump_dir"], fileName)

        print("Started importing database \"{0}\" from file: {1}".format(dbName, filePath))
        self.system.cmd("cat \"{2}\" | docker exec -i {0} mysql --login-path=client --database={1}".format(container, dbName, filePath))
        print("Import completed")

        return TerminalStatus.stop

    def MySQL_Export(self):
        if not self.hasAuthorize():
            return TerminalStatus.abort

        print("Export database.\n")

        self.databases = self.getDatabases()
        self.sqlfiles = self.getListDir()

        dbName = self.system.input("Database name: ", self.Input_Database)
        fileName = self.system.input("Import from file: ", self.Input_File)

        if not dbName or not fileName:
            return TerminalStatus.abort

        container = self.config["container"]
        exportPath = os.path.join(self.config["dump_dir"], fileName)

        print("Started exporting database \"{0}\" to file: {1}".format(dbName, exportPath))
        self.system.cmd("docker exec {0} mysqldump --login-path=client {1} > \"{2}\"".format(container, dbName, exportPath))
        print("Export completed")

        return TerminalStatus.stop

    def MySQL_Drop(self):
        if not self.hasAuthorize():
            return TerminalStatus.abort

        print("Delete database.\n")

        self.databases = self.getDatabases()

        dbName = self.system.input("Database name: ", self.Input_Database)

        if not dbName:
            return TerminalStatus.abort

        if dbName not in self.databases:
            raise Exception("The \"{0}\" database does not exists.".format(dbName))

        output = self.execute("DROP DATABASE IF EXISTS \`{0}\`;".format(dbName))
        if len(output) > 0:
            raise Exception(output)
        print("Database \"{0}\" was removed.".format(dbName))

        return TerminalStatus.stop

    def execute(self, command):
        execute = "docker exec -i {0} mysql --login-path=client --execute=\"{1}\""
        return self.system.subprocess(execute.format(self.config["container"], command))

    def Input_Database(self, text, state):
        completions = []
        for str in self.databases:
            if str.startswith(text):
                completions.append(str)
        return completions[state]

    def Input_File(self, text, state):
        completions = []
        for str in self.sqlfiles:
            if str.startswith(text):
                completions.append(str)
        return completions[state]

    def getDatabases(self):
        dbList = self.execute("SHOW DATABASES;").split("\n")[1:]
        if "display_system_databases" not in self.config:
            dbExclude = ['information_schema', 'mysql', 'performance_schema', 'sys']
            dbList = list(filter(lambda score: score not in dbExclude, dbList))
        return dbList

    def getListDir(self):
        filesList = []
        if "dump_dir" in self.config and os.path.exists(self.config["dump_dir"]):
            for fileName in os.listdir(self.config["dump_dir"]):
                filePath = os.path.join(self.config["dump_dir"], fileName)
                if os.path.isfile(filePath) and filePath.endswith(".sql"):
                    filesList.append(fileName)
        return filesList
