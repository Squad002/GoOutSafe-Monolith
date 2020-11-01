[![Build Status](https://travis-ci.org/reuseman/GoOutSafe.svg?branch=main)](https://travis-ci.org/reuseman/GoOutSafe) [![Coverage Status](https://coveralls.io/repos/github/reuseman/GoOutSafe/badge.svg?branch=main)](https://coveralls.io/github/reuseman/GoOutSafe?branch=main) [![Requirements Status](https://requires.io/github/reuseman/GoOutSafe/requirements.svg?branch=main)](https://requires.io/github/reuseman/GoOutSafe/requirements/?branch=main)

## Getting started
Instructions for the **Developers**

### VS Code
In order to have a consistent coding style, formatting on save, good spelling:

1. Let's use the **workspace** feature.

    File -> Open Workspace -> .vscode/python-dev.code-workspace
2. Install the recommended extensions (feel free to propose new ones).
    
### Docker
    docker build -t gooutsafe:latest . 
    docker run --name gooutsafe -d -p 8000:5000 --rm gooutsafe:latest
    http://127.0.0.1:5000

### Prerequisites
    pip install -r requirements/dev.txt
    
### Running
    export FLASK_APP=monolith/app.py 
    flask run

### Manually generate mock data in the database
    flask shell
    from monolith import mock
    mock.restaurant()
    mock.restaurant()

### To run tests with coverage
Inside GoOutSafe run (it will automatically use the configuration in pyproject.toml):

    pytest

If you want to see an interactive report run:

    coverage html

## User stories
![](docs/user-stories.png)

## E-R Diagram in PlantUML
![](docs/plantUML-er.png)