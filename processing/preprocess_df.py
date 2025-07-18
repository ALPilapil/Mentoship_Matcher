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

def preprocessing_df(df):
    # remove anything irrelevant to matching
    # make all the columns lowercase
    df.rename(columns=str.lower, inplace=True)

    # make all the stuff in the cells lower
    df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

    # remove everything that isn't alphanumeric or a space
    df = keep_alpha_num(df)
    
    return df