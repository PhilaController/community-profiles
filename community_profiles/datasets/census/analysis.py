import numpy as np


def calculate_cv(df):
    """
    Calculate the coefficient of variation for the input 
    Census data
    """
    # Get the non-geographic cols
    cols = df.filter(regex="^(?!geo)\w*$(?<!moe)", axis=1).columns

    # Only use cols with a _moe pair
    cols = [col for col in cols if f"{col}_moe" in df.columns]

    # standard error
    SEs = df[[f"{col}_moe" for col in cols]].values / 1.645

    # values
    values = df[cols].values
    values[values == 0.0] = np.nan  # handle zeros separately

    # coefficient of variation
    CVs = SEs / values

    # output
    out = df.copy()
    out = out[[col for col in out.columns if col.startswith("geo") or col in cols]]

    # copy over CVs
    out[cols] = CVs
    return out

