# Train/validation/test splitting
# Goal: Robust evaluation and backtesting.
# - Approach: Time‑based split.



def time_split(df, train_end, val_end):
    train = df[df.index <= train_end]
    val = df[(df.index > train_end) & (df.index <= val_end)]
    test = df[df.index > val_end]
    return train, val, test