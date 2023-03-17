"Delete this if it is outside the scope of the project."


def cross_val():
    """Choose the cross-validation subsets.

    Return:
        k_fold ():

    """
    k_fold = KFold(n_splits=10, shuffle=True, random_state=42)
    return k_fold


def model_fit(k_fold, data=split(data_model)):
    param_grid = {"C": [0.1, 1, 10, 100], "penalty": ["l2"]}
    model = LogisticRegression(random_state=42)
    grid = GridSearchCV(model, param_grid, cv=k_fold)
    model_fit = grid.fit(data[0], data[1])
    return model_fit


@pytask.mark.depends_on(
    {
        "fit": ["model.py"],
        "pred": ["predict.py"],
        "data_model": BLD / "python" / "data" / "data_model.pkl",
        "data_model_pred": BLD / "python" / "data" / "data_model_pred.pkl",
        "data_benchmark": BLD / "python" / "data" / "data_benchmark.pkl",
        "data_benchmark_pred": BLD / "python" / "data" / "data_benchmark_pred.pkl",
    },
)
@pytask.mark.task
@pytask.mark.produces(BLD / "python" / "data" / "concatenated_pred.csv")
def task_produce_data(depends_on, produces):
    data_model = pd.read_pickle(depends_on["data_model"])
    data_model_pred = pd.read_pickle(depends_on["data_model_pred"])
    data_benchmark = pd.read_pickle(depends_on["data_benchmark"])
    data_benchmark_pred = pd.read_pickle(depends_on["data_benchmark_pred"])
    # if name == "scores_pred":
    predicted_df = concatenate_dfs(
        data_model,
        data_model_pred,
        data_benchmark,
        data_benchmark_pred,
    )
    predicted_df.to_csv(produces)


@pytask.mark.try_first
@pytask.mark.depends_on(
    {
        "scripts": ["scraper.py"],
    },
)
@pytask.mark.task
# @pytask.mark.produces(BLD / "python" / "scrapes" / f"{month}_{scrapedate()}.html")
def task_produce_scrape(depends_on):
    url_start = "https://www.basketball-reference.com/leagues/NBA_2023_games-{}.html"
    scraper_by_month(months, url_start, date.today())
