# MakeMyDay

Web application for creating and managing time tables.

***

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Setting up the global environment

Before starting development, you need to make sure that you have Python 3.8 installed. You can check the version by opening cmd and executing `python --version`. If it refers to nothing or Python different than 3.8, you need to [download Python](https://www.python.org/downloads/) and make sure it's available through the `python` alias in CMD. 

The next step requires installing [Visual Studio Code](https://code.visualstudio.com), an [extension for Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) language server. There are some nice to have extensions as well:
- [Task Explorer](https://marketplace.visualstudio.com/items?itemName=spmeesseman.vscode-taskexplorer)
- [Bracket Pair Colorizer 2](https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer-2)
- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
- [Trailing spaces](https://marketplace.visualstudio.com/items?itemName=shardulm94.trailing-spaces)

Once you have extensions installed, you need to make sure that your default terminal in VS Code is a standard `Windows CMD`. To achieve it, press `ctrl + shift + p` in Visual Studio Code. It will open a prompt in the top bar. Type `Terminal: Select Default Shell` there, confirm with `enter`, choose `Command Prompt` from the list and confirm with `enter` again.

### Setting up the local environment

Simply open Visual Studio Code in the root directory, press `ctrl + shift + p`, type `Tasks: run task` and confirm it with `enter`. It will show a list of all available tasks. Choose `Python: set up environment` and press `enter`. You'll see a dropdown with choices, select `Continue without scanning the task output` and press `enter` again. It should open a terminal and install all the required packages (alternatively, you can use the Task Explorer extension for that).

The next step is to prepare Django for local development. First of all, you need to run the database's migrations by executing `Django: Migrate` tasks. Once this is ready, you should create a superuser. Open a new terminal in Visual Studio Code by going to the `Terminal` tab and selecting `New terminal` (or CTRL+SHIFT+\`). The path in the terminal window should be prepended with the `(.venv)` keyword. If it's not, you need to activate the virtual environment by executing `.venv\Scripts\activate`. Finally, create the superuser by executing `python manage.py createsuperuser` and follow the prompts.

## Running the tests

### Unit-Testing

To execute all tests you need to click on the `Run` view in the `activity bar` (alternatively, press `ctrl + shift + d`) and execute `Django: Tests` configuration.

### Local server

If you want to run the project on a local server you should also go to the `Run` view and execute `Django: Run server` configuration.

### Maintaining code quality

Make sure to execute `Python: Linter` run configuration after applying changes so that you can catch all potential syntactical and stylistic problems.


***

## Built With

* [Python](https://www.python.org) - Main programing language
* [Django](https://www.djangoproject.com) - Web framework
* [PIP](https://pip.pypa.io/) - Dependency Management
* [Visual Studio Code](https://code.visualstudio.com) - IDE and process management

***

## Contributing

Before committing anything, you need to create an issue in the [Feature Board](https://github.com/kucharzyk-sebastian/make-my-day/projects/1) and use its number as your feature branch's name.

***

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/montrosesoftware/sayThumbsApp-serverless/tags).

***

## Authors

* [Sebastian Kucharzyk](https://github.com/kucharzyk-sebastian)
* [Mateusz Olejarz](https://github.com/mateusz-olejarz)

See also the list of [contributors](https://github.com/kucharzyk-sebastian/make-my-day/graphs/contributors) who participated in this project.
