# Scraping basketball data to predict future game outcomes

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/NormProgr/bask/main.svg)](https://results.pre-commit.ci/latest/github/NormProgr/bask/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Authors
- Norman Metzinger
- Anne Rebecca Ringborg

## About
This is a project that aims to predict the probability of a team winning or losing a game in the 2022/23 NBA season using logistic regression and web scraping. The project utilizes data from [Basketball Reference](https://www.basketball-reference.com/leagues/NBA_2023_games-{}.html) to collect the necessary information for each game such as points, teams, viewer attendance, etc. The data is summarized in an information sheet.

To obtain the required data for the analysis, the project utilizes web scraping techniques to extract up-to-date information. The collected data is then cleaned, pre-processed, and fed into the logistic regression model for analysis.

The project is implemented in Python, utilizing various libraries such as Scikit-learn, Pandas, and BeautifulSoup for data processing, modeling, and web scraping respectively. The code is well documented and organized with Pytask for ease of understanding and modification. In the following, we describe how to replicate the whole project.

The goal of this project is to provide an automated prediction tool for NBA fans and enthusiasts to make informed decisions when betting or discussing NBA games. The predictions are updated every time the code is run, ensuring that users have access to the latest and most accurate information when making their predictions.

## Usage

To run this project a Python and a LaTex distribution is required. The project was tested on windows 11 and macOS 10.15.7 with Python 3.11.0. All further dependencies are included in the environment.

To get started, create and activate the environment with

```console
$ conda env create -f environment.yml
$ conda activate bask
```

To build the project, type

```console
$ pytask
```

### For code development

To run tests

```console
$ pytest
```

To set-up workflow hooks

```console
$ pre-commit install
```

## Project structure

Within the *src/bask* directory all relevant code files can be found. They are structured as follows:
- *analysis*: Summary of all analysis files.
  - *evaluation.py*: Benchmark analysis of NBA games.
  - *model.py*: Build the logistic regression model.
  - *predict.py*: Predict the future games outcomes.
  - *task_analysis.py*: Run all analysis files. 
- *data*: all not build source files
- *data_management*: Summary data pre-processes.
  - *clean_data.py*: Data pre-processing.
  - *task_data_management.py*: Run the clean data file.
- *final*: Summary of data visualizations and tables.
  - *plot.py*: Produce all plots.
  - *task_final.py*: Produce final prediciton and model results.
- *preparation*: Contains the web-scraper.
  - *parser.py*: Translates html to pickle.
  - *scraper.py*: Scrapes the data from the website.
  - *task_preparation.py*: Runs all preparation files.

Additionally the *paper/task_paper.py* is producing the NBA prediction infromation sheet.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
