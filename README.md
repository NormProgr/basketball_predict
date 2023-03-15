# Scraping basketball data to predict future game outcomes

This project predicts the probability of a team winning or losing a basketball game in
the 2022/23 NBA season using a logistic regression, web scraping the results of past
games from www.basketball-reference.com.

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/NormProgr/bask/main.svg)](https://results.pre-commit.ci/latest/github/NormProgr/bask/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Usage

The project was implemented in Python 3.11.0 on macOS Ventura 13.0.1 and Windows 11
using Visual Studio Code. The packages required for this project can be found in the
file environment.yaml. Since the data is scraped within the code, our results are
replicable by running pytask, as long as the url source remains accurate. After the end
of the NBA season (9th April 2023), the project can still be used to evaluate the
quality of predictions, even if no future games remain. To reproduce our project, one
can follow these steps:

1. Install Anaconda and Visual Code Studio
   (https://docs.anaconda.com/anaconda/install/index.html,
   https://code.visualstudio.com/download)
1. Clone the repository
1. Create and activate the project environment with

```console
$ conda/mamba env create
$ conda activate bask
```

4. To build the project, type

```console
$ pytask
```

Details on implementation and results can be found in bask.pdf after running the
project.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
