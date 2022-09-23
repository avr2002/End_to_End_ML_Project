from tkinter import E
import yaml
from housing.exception import HousingException
import os, sys
import numpy as np
import pandas as pd
import dill
from housing.constant import *

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e 


def load_data(file_path:str, schema_file_path:str)->pd.DataFrame:
        """
        We are loading the data for transformation and changing it's column datatype according to schema.yaml file.
        """
        try:
            dataset_schema = read_yaml_file(schema_file_path)
            schema = dataset_schema[DATASET_SCHEMA_COLUMN_KEY]

            df = pd.read_csv(file_path)

            error_message = ""

            for column in df.columns:
                if column in list(schema.keys()):
                    df[column].astype(schema[column])
                else:
                    error_message = f"{error_message} \nColumn: [{column}] is not in the schema file."
            
            if len(error_message)>0:
                raise Exception(error_message)
            return df
        except Exception as e:
            raise HousingException(e,sys) from e


def save_numpy_array_data(file_path:str, array:np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HousingException(e,sys) from e 

def load_numpy_array_data(file_path:str)->np.array:
    """
    Load numpy array data from file
    file_path: str location of file to load
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e 

def save_object(file_path:str, obj):
    """
    file_path: str
    obj: Any sort of object to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e 

def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e 