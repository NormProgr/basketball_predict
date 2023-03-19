# Scraping basketball data to predict future game outcomes

[![pre-commit.ci passed](https://img.shields.io/badge/pre--commit.ci-passed-brightgreen)](https://results.pre-commit.ci/run/github/274689747/1678058970.SI-lnarDSRqXafVBdLucmg)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![image](https://img.shields.io/badge/pytask-v0.3.1-red)](https://pypi.org/project/pytask/)
[![image](https://img.shields.io/badge/python-3.11.0-blue)](https://www.python.org/)
[![image](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/license/mit/)
[![image](https://img.shields.io/badge/LaTeX-v0.3.0-yellowgreen)](https://www.tug.org/texlive/)
[![image](https://img.shields.io/badge/platform-osx--64%20%20%2F%20win--64-lightgrey)](<>)
[![image](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/NormProgr/basketball_predict)
[![image](https://img.shields.io/badge/pytest-v7.2.2-orange)](https://docs.pytest.org/en/7.2.x/)


## Authors

- Norman Lothar Metzinger, 3501090
- Anne Rebecca Charlotte Ringborg, 3069618

## About

This project predicts the probability of a team winning or losing a game in the 2022/23
NBA season using logistic regression and web scraping. The project uses data from
[Basketball Reference](https://www.basketball-reference.com/leagues/NBA_2023_games-%7B%7D.html)
to collect the necessary information for each game such as points, teams, etc. The
results are summarized in an information sheet when running the project.

To obtain the required data for the analysis, the project uses web scraping to extract
up-to-date information. The collected data is cleaned, pre-processed, and fed into the
logistic regression model for analysis. Data from games until the 15th February are used
for the model fit. Game results for after this date are predicted and the results up to
the current scrape are used to evaluate the prediction quality. After the end of the NBA
season (9th April 2023), the project can still be used to evaluate the quality of
predictions, even if no future games remain.

In the absence of a internet connection, the code uses old scrapes for prediction, if
they exist. Thus, an active connection is not necessary to run the project after the
initial setup and first run.

The project is implemented in Python, using various libraries such as Scikit-learn,
Pandas, and BeautifulSoup for data processing, modeling, and web scraping respectively.
The code is documented and organized with [pytask](https://github.com/pytask-dev/pytask)
for intuition and easy modification. In the following, we describe how to replicate the
whole project.

## Usage

To run this project, a Python and a LaTex distribution are required. The project was
implemented in Python 3.11.0 on macOS Ventura 13.0.1 and Windows 11 using Visual Studio
Code. All further dependencies are included in the environment. Since the data is
scraped within the code, our results are replicable by running
[pytask](https://github.com/pytask-dev/pytask).

To reproduce the project, one can follow these steps:

1. Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html),
   [Git](https://git-scm.com/),
   [Visual Code Studio](https://code.visualstudio.com/download), and a LaTeX
   distribution such as [TeX Live](https://www.tug.org/texlive/)
1. Clone the repository
1. Create and activate the project environment with

```console
$ conda env create -f environment.yml
$ conda activate bask
```

4. To build the project, type

```console
$ pytask
```

Details on implementation and results can be found in *bask.pdf* after running the
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

The relevant code files can be found in the *src/bask* directory. They are structured as
follows:

- *analysis*: All analysis code files.
  - *evaluation.py*: Benchmark analysis of NBA games.
  - *model.py*: Build the logistic regression model.
  - *predict.py*: Predict the future game outcomes.
  - *task_analysis.py*: Run all analysis files.
- *data*: Source files that are not built.
- *data_management*: Data pre-processing.
  - *clean_data.py*: Functions for pre-processing.
  - *task_data_management.py*: Run the clean_data file.
- *final*: Data visualizations and tables.
  - *plot.py*: Functions for plots.
  - *task_final.py*: Produce final results and plots.
- *preparation*: Web scraping.
  - *parser.py*: Translate html to pickle.
  - *scraper.py*: Scrape the data from the website.
  - *task_preparation.py*: Run all preparation files.

Additionally the *paper/task_paper.py* is producing the NBA prediction information
sheet.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
This project uses [pytask](https://github.com/pytask-dev/pytask) as workflow management.
Some inspiration was taken from OpenAI's [ChatGTP 3.5](https://openai.com/blog/chatgpt)
and, obviously, [stackoverflow](https://stackoverflow.com).
