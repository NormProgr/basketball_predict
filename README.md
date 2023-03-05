# Scraping basketball data to predict future game outcomes

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/NormProgr/bask/main.svg)](https://results.pre-commit.ci/latest/github/NormProgr/bask/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Authors
- Norman Metzinger
- Anne Rebecca Ringborg

## About
This is a project that aims to predict the probability of a team winning or losing a game in the current NBA season using logistic regression and web scraping. The project utilizes data from various sources such as NBA official website and basketball-reference.com to collect the necessary information for each game such as team stats, player stats, game venue, etc.

To obtain the required data for the analysis, the project utilizes web scraping techniques to extract information from various sources in real-time. The collected data is then cleaned, pre-processed, and fed into the logistic regression model for analysis.

The project is implemented in Python, utilizing various libraries such as Scikit-learn, Pandas, and BeautifulSoup for data processing, modeling, and web scraping respectively. The code is well documented and organized with pytask for ease of understanding and modification.

The goal of this project is to provide a reliable and accurate prediction tool for NBA fans and enthusiasts to make informed decisions when betting on NBA games. The predictions are updated every time the code is run, ensuring that users have access to the latest and most accurate information when making their predictions.

## Usage

To get started, create and activate the environment with

```console
$ conda/mamba env create
$ conda activate bask
```

To build the project, type

```console
$ pytask
```

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
