def remove_irrev(df, irrev_cols):
    # get the names of the irrelevent cols
    original_columns = df.columns
    columns_to_drop = []

    for x in original_columns:
        for y in irrev_cols:
            if y in x:
                columns_to_drop.append(x)

    # drop these cols
    df.drop(columns=columns_to_drop, inplace=True)

def keep_alpha_num(df):
    # go to each cell
    nrows = df.shape[0]
    ncols = df.shape[1]

    for i in range(nrows):
        for j in range(ncols):
            cell = df.iloc[i,j]
            if isinstance(cell, str):
                for ch in cell:
                    if not (ch.isalnum() or ch.isspace()):
                        cell = cell.replace(ch,"")
                df.iat[i, j] = cell

    return df

def preprocessing_df(df, irrev_cols):
    # remove anything irrelevant to matching
    # make all the columns lowercase
    df.rename(columns=str.lower, inplace=True)

    # remove irrelevant columns
    remove_irrev(df,irrev_cols)

    # make all the stuff in the cells lower
    df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

    # remove everything that isn't alphanumeric or a space
    df = keep_alpha_num(df)
    
    return df