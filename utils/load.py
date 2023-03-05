import os
from pathlib import Path
import pandas as pd
from pandas_profiling import ProfileReport


def load_data(file_name, folder_name=None):
    parent_path = Path(os.getcwd()).parent
    if folder_name:
        # path = parent_path / folder_name / file_name
        path = Path("/".join([os.getcwd(), folder_name, file_name]))
    else:
        # path = parent_path / file_name
        path = Path("/".join([os.getcwd(), file_name]))
    
    file_type = file_name.split(".")[1]
    if file_type=="csv":
        output = pd.read_csv(path)
    elif file_type== "xlsx":
        output = pd.read_excel(path)
    else:
        raise f"Failed to load data - invalid file type {file_type}"
    
    return output