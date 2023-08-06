# Docker Projects
Application for easy project management based on "docker-compose". All projects in one terminal with a set of useful tools. Powered by Python 3.

## Get Started
1. Download file **docker.pyc**.
2. Create file **projects.json** next to **docker.pyc**. The file is a regular JSON file.
3. Add project parameters to **projects.json** using the instructions below.
4. Run **docker.pyc** using terminal command: **python3 docker.pyc**.

## How to add new project
To add more projects, simply add a new block with project properties, following the JSON structure.
```json
[
    {
        "name": "Best project",
        "docker": "/home/user/project/docker",
        "tools": {}
    }
]
```
  - **name** [recommended] - Project name.
  - **docker** [required] - The full path of the directory where it is located **docker-compose.yml**.
  - **tools** [optional] - Configuration of additional tools.

## Base commands
Each command contains a sequence number (e.g. 1, 2, 3). To run the desired command, type the number and press **Enter**.
The command may contain subcommands. In this case, you need to specify the command number and its subcommand using a dot to separate it (e.g. 1.1, 2.1, 3.5).
You can also use special commands (e.g. help, notify, mysql, exit).

_Commands are not available inside a docker container._

List of basic commands to control current shell.
  - **exit, x, 0** - Close current shell.
  - **help, h** - Display documentation of current shell.
  - **notify, n** - Show system notification.

## Project Tools
A set of tools for projects. Add the necessary configuration to connect the instrument.
If there is no tool configuration, the tool will not display and run.

#### Magento Tools Instruction
A tool for easy viewing and running Magento 2 CLI commands. You can run a queue with multiple commands.
To start a queue of multiple commands, use a semicolon (;) to separate the commands.
```json
[
    {
        "name": "Best project",
        "docker": "/home/user/project/docker",
        "tools": {
            "magento": {
                "container": "magento2_php",
                "user": "john",
                "hide_groups": ["downloadable", "encryption", "i18n"]
            }
        }
    }
]
```
  - **container** [required] - PHP container name.
  - **user** [recommended] - The user on behalf of which the commands will be executed (e.g. www-data).
  - **hide_groups** [optional] - Groups of commands to hide.

#### Xdebug Tools Instruction
Allows you to manage the Xdebug module. Disable Xdebug when you don't need it, it will speed up PHP.
```json
[
    {
        "name": "Best project",
        "docker": "/home/user/project/docker",
        "tools": {
            "xdebug": {
                "container": "magento2_php"
            }
        }
    }
]
```
  - **container** [required] - PHP container name.

#### MySQL Tools Instruction
Allows you to manage the MySQL (e.g. create/delete/import/export database).
```json
[
    {
        "name": "Best project",
        "docker": "/home/user/project/docker",
        "tools": {
            "mysql": {
                "container": "magento2_mysql",
                "user": "root",
                "dump_dir": "/home/user/project/mysql_dumps",
                "display_system_databases": true,
                "users": ["admin"]
            }
        }
    }
]
```
  - **container** [required] - MySQL container name.
  - **user** [required] - The username to access the database.
  - **dump_dir** [recommended] - Path to the directory for import and export.
  - **display_system_databases** [optional] - Show system databases (e.g. information_schema, mysql, performance_schema, sys).
  - **users** [optional] - Additional users that are created in MySQL. After creating a new database, these users will have all privileges to this database.

#### ElasticSearch Tools Instruction
Allows you to manage the ElasticSearch.
```json
[
    {
        "name": "Best project",
        "docker": "/home/user/project/docker",
        "tools": {
            "elasticsearch": {
                "container": "magento2_elasticsearch"
            }
        }
    }
]
```
  - **container** [required] - Elasticsearch container name.

#### Redis Tools Instruction
Allows you to manage the Redis.
```json
[
    {
        "name": "Best project",
        "docker": "/home/user/project/docker",
        "tools": {
            "redis": {
                "container": "magento2_redis"
            }
        }
    }
]
```
  - **container** [required] - Redis container name.

### Desktop - Linux
You can create desktop link
1. Open folder: ~/.local/share/applications
2. Create file with name: docker-projects.desktop
3. File content the next:
```ini
[Desktop Entry]
Version=1.0
Name=Docker Projects
Comment=Terminal for docker projects
Exec=python3 /home/user/projects/docker.pyc
Icon=/home/user/projects/docker.png
Path=/home/user/projects
Terminal=true
Type=Application
Categories=Application;
```
