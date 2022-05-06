from typing import List

import pandas as pd

from scipy import stats

def remove_outiliers(frame: pd.DataFrame, column: str, type:str='iqr') -> pd.DataFrame:

    '''
    This function remove outliers, today the only method is using IQR
    
    Args:

    frame - The dataframe for remove the outliers
    column - column name used for remove the outliers, the column values
    must be numbers (int, float)

    Returns
    
    Return the passed DataFrame without outlier
    '''
    column_type = frame.loc[:, column].dtype

    assert isinstance(column_type, float) or isinstance(column_type, int),\
         f"Column passe have type diferrent of int or float. Type: {column_type}" #to verify if this was correct implementation

    if type == 'iqr':
        iqr = stats.iqr(frame[~pd.isnull(frame.loc[:, column]), column])

        p25 = frame[~pd.isnull(frame.loc[:, column]), column].quantile(0.25)

        p75 = frame[~pd.isnull(frame.loc[:, column]), column].quantile(0.75)

        frame_w_ol = frame.query(f"{p25 - 1.5*iqr} <= {column} "
                                f"<= {iqr + 1.5*p75}").copy()

        return frame_w_ol
    else:
        raise TypeError("Only implemented IQR type")


def factorize_columns(frame: pd.DataFrame, columns: List[str]) -> dict:

    '''
    This function factorizes the columns that are passed as argument

    The Dataframe is factorized in place, the columns name will be
    numerical_{column_name
    
    Args:

    frame - The dataframe for insert the factorize columns
    columns - columns to be factorize

    Returns:

    Maping beetwen unique values and code the dict have this format:

    code_unique_map = {
        column_name: [code, unique values]
    }
    
    
    '''

    code_unique_map = {}

    for column in column:

        column_code, column_unique =  pd.factorize(frame.loc[:, column])
        frame.loc[:, f"numerical_{column}"] = column_code

        code_unique_map[column] = [column_code, column_unique]

    return code_unique_map
    