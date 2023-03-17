# Scraping basketball data to predict future game outcomes

[![pre-commit.ci passed](https://results.pre-commit.ci/badge/github/NormProgr/bask/main.svg)](https://results.pre-commit.ci/latest/github/NormProgr/bask/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![image](https://img.shields.io/badge/pytask-workflow-red)](https://img.shields.io/badge/pytask-workflow-red)


## Authors

- Norman Metzinger
- Anne Rebecca Charlotte Ringborg

## About

This project predicts the probability of a team winning or losing a game in the 2022/23
NBA season using logistic regression and web scraping. The project uses data from
[Basketball Reference](https://www.basketball-reference.com/leagues/NBA_2023_games-%7B%7D.html)
to collect the necessary information for each game such as points, teams, viewer
attendance, etc. The data is summarized in an information sheet.

To obtain the required data for the analysis, the project utilizes web scraping
techniques to extract up-to-date information. The collected data is then cleaned,
pre-processed, and fed into the logistic regression model for analysis. After the end of
the NBA season (9th April 2023), the project can still be used to evaluate the quality
of predictions, even if no future games remain.

The project is implemented in Python, utilizing various libraries such as Scikit-learn,
Pandas, and BeautifulSoup for data processing, modeling, and web scraping respectively.
The code is well documented and organized with Pytask for ease of understanding and
modification. In the following, we describe how to replicate the whole project.

The goal of this project is to provide an automated prediction tool for NBA fans and
enthusiasts to make informed decisions when betting or discussing NBA games. The
predictions are updated every time the code is run, ensuring that users have access to
the latest and most accurate information when making their predictions.

## Usage

To run this project, a Python and a LaTex distribution are required. The project was
implemented in Python 3.11.0 on macOS Ventura 13.0.1 and Windows 11 using Visual Studio
Code. All further dependencies are included in the environment. Since the data is
scraped within the code, our results are replicable by running pytask.

To reproduce the project, one can follow these steps:

1. Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html),
   [Git](https://git-scm.com/) and
   [Visual Code Studio](https://code.visualstudio.com/download)
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

Within the *src/bask* directory all relevant code files can be found. They are
structured as follows:

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

Additionally the *paper/task_paper.py* is producing the NBA prediction information
sheet.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
This project uses [pytask](https://github.com/pytask-dev/pytask) as workflow management.
