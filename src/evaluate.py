# evaluate.py — model performance plots for the 5 CO2-pressure regression models
# Uses the output of mof_models.evaluate_target_columns() as input

# import matplotlib for all plotting
import matplotlib.pyplot as plt
# import numpy for array math (residuals, axis limits)
import numpy as np


def plot_parity(results, y_true_by_target, split="test", save_path=None):
    """Predicted vs actual scatter, one panel per target, with a y=x reference line."""
    # get the list of target column names from the results dict keys
    targets = list(results.keys())
    # set up a grid wide enough for all targets, capped at 3 columns per row
    n_cols = min(3, len(targets))
    # compute how many rows are needed given n_cols
    n_rows = int(np.ceil(len(targets) / n_cols))
    # create the figure and one subplot axis per target
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4.5 * n_rows))
    # flatten axes to a 1D array so we can index it with a simple loop counter
    axes = np.array(axes).reshape(-1)

    # loop through each target and its subplot axis together
    for ax, target in zip(axes, targets):
        # predicted values for this target/split come from the stored results
        y_pred = results[target]["predictions"][split]
        # actual values must be passed in separately (not stored in results)
        y_true = y_true_by_target[target][split]
        # scatter actual (x-axis) vs predicted (y-axis)
        ax.scatter(y_true, y_pred, alpha=0.3, s=12, color="#028090")
        # draw the y=x reference line across the full data range
        lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
        ax.plot(lims, lims, color="#990011", linewidth=1.2, linestyle="--")
        # label the axes and title with the target name and split
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.set_title(f"{target} ({split})", fontsize=10)

    # hide any unused subplot axes if targets don't fill the grid evenly
    for ax in axes[len(targets):]:
        ax.axis("off")

    # tighten layout so titles/labels don't overlap between panels
    fig.tight_layout()
    # save to disk if a path was given, otherwise just show it
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_residuals(results, y_true_by_target, split="test", save_path=None):
    """Residuals (actual - predicted) vs predicted, one panel per target."""
    # get target names in the same order as the results dict
    targets = list(results.keys())
    # same grid setup as plot_parity
    n_cols = min(3, len(targets))
    n_rows = int(np.ceil(len(targets) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4.5 * n_rows))
    axes = np.array(axes).reshape(-1)

    for ax, target in zip(axes, targets):
        # predicted values for this target/split come from the stored results
        y_pred = results[target]["predictions"][split]
        # actual values must be passed in separately (not stored in results)
        y_true = y_true_by_target[target][split]
        # compute residuals as actual minus predicted
        residuals = y_true - y_pred
        # scatter residuals against predicted values
        ax.scatter(y_pred, residuals, alpha=0.3, s=12, color="#00A896")
        # draw a horizontal line at zero residual for reference
        ax.axhline(0, color="#990011", linewidth=1.2, linestyle="--")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Residual (actual - predicted)")
        ax.set_title(f"{target} ({split})", fontsize=10)

    for ax in axes[len(targets):]:
        ax.axis("off")

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_r2_comparison(summary_df, save_path=None):
    """Grouped bar chart comparing train/valid/test R2 across all 5 targets."""
    # shorten target labels for x-axis (strip common prefix/suffix)
    labels = summary_df["target"].str.replace("CO2_uptake_", "", regex=False).str.replace("_molkg", "", regex=False)
    # x positions for each group of bars
    x = np.arange(len(labels))
    # width of each individual bar within a group
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 5))
    # plot train R2 bars, shifted left
    ax.bar(x - width, summary_df["train_r2"], width, label="Train", color="#028090")
    # plot valid R2 bars, centered
    ax.bar(x, summary_df["valid_r2"], width, label="Valid", color="#00A896")
    # plot test R2 bars, shifted right
    ax.bar(x + width, summary_df["test_r2"], width, label="Test", color="#02C39A")

    # set x-axis tick labels to the shortened pressure names
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0)
    ax.set_ylabel("R²")
    ax.set_title("Train / Valid / Test R² by pressure target")
    ax.legend()
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


# ---- example usage (run this file directly to test on your real results) ----
if __name__ == "__main__":
    # import your existing modeling functions
    from mof_models import evaluate_target_columns
    # import pandas to load your cleaned dataset
    import pandas as pd

    # load your combined structural + CO2 dataset
    df = pd.read_csv("data/processed/hmof_clean.csv")

    feature_columns = ["lcd", "pld", "void_fraction", "surface_area_m2g"]
    target_columns = [
        "CO2_uptake_0.01bar_molkg", "CO2_uptake_0.05bar_molkg",
        "CO2_uptake_0.1bar_molkg", "CO2_uptake_0.5bar_molkg",
        "CO2_uptake_2.5bar_molkg",
    ]
    rf_params = dict(n_estimators=100, max_depth=None, min_samples_split=2,
                      min_samples_leaf=1, random_state=12345, n_jobs=-1)

    # run the evaluation across all 5 targets (this returns models + metrics + predictions)
    results, summary = evaluate_target_columns(df, feature_columns, target_columns, rf_params)

    # build a y_true_by_target dict since results only stores predictions, not actuals
    # (train_and_evaluate_random_forest fits on the same splits each time, so we rebuild them here)
    from mof_models import split_target_data
    y_true_by_target = {}
    for target in target_columns:
        X_train, X_valid, X_test, y_train, y_valid, y_test = split_target_data(df, feature_columns, target)
        y_true_by_target[target] = {"train": y_train, "valid": y_valid, "test": y_test}

    # generate and save all three plots
    plot_parity(results, y_true_by_target, split="test",
                save_path="reports/parity_test.png")
    plot_residuals(results, y_true_by_target, split="test",
                    save_path="reports/residuals_test.png")
    plot_r2_comparison(summary, save_path="reports/r2_comparison.png")
