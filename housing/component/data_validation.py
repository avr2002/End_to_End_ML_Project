import os,sys
import pandas as pd
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from housing.util.util import read_yaml_file

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json 

class DataValidation:
    
    def __init__(self, data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info("Data Validation Started!")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_train_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training & testing file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist

            logging.info(f"Is train & test file exists? -> {is_available}")

            if not is_available:
                message = f"Training file: {train_file_path} or Testing file: {test_file_path} is Not Present!"
                # logging.info(message)
                raise Exception(message)
            
            return is_available
        except Exception as e:
            raise HousingException(e,sys) from e

    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False
            #Assigment validate training and testing dataset using schema file
            #1. Number of Columns #2. Check the value of ocean proximity acceptable values:[<1H OCEAN, INLAND, ISLAND, NEAR BAY, NEAR OCEAN] #3. Check column names
            schema_file = read_yaml_file(self.data_validation_config.schema_file_path)
            train_df, test_df = self.get_train_test_df()

            logging.info("Checking train & test set from schema file")
            # Checking number of columns in train-test set
            # is_num_of_cols_same = train_df.shape[1] == test_df.shape[1] == len(schema_file['columns'])
            is_num_of_cols_same_trainSet = train_df.shape[1] == len(schema_file['columns'])
            is_ocean_proximity_values_same_trainSet = sorted(train_df['ocean_proximity'].unique().tolist()) == sorted(schema_file['domain_value']['ocean_proximity'])
            is_column_names_same_trainSet= sorted(train_df.columns.to_list()) == sorted(schema_file['columns'])

            is_num_of_cols_same_testSet = test_df.shape[1] == len(schema_file['columns'])
            is_ocean_proximity_values_same_testSet = sorted(test_df['ocean_proximity'].unique().tolist()) == sorted(schema_file['domain_value']['ocean_proximity'])
            is_column_names_same_testSet = sorted(test_df.columns.to_list()) == sorted(schema_file['columns'])

            validation_status_for_trainSet = is_num_of_cols_same_trainSet and is_ocean_proximity_values_same_trainSet and is_column_names_same_trainSet
            validation_status_for_testSet = is_num_of_cols_same_testSet and is_ocean_proximity_values_same_testSet and is_column_names_same_testSet
            validation_status = validation_status_for_trainSet and validation_status_for_testSet

            logging.info(f"Data Validation Complete: Validation Status: {validation_status}")

            if validation_status==False:
                message = f"Validation Status:{validation_status}. Either train or test set is not valid! Please Check!\
                    \nTrain Set Validation Status:\
                    {validation_status_for_trainSet} & Test Set Validation Status: {validation_status_for_testSet}"
                raise Exception(message)

            return validation_status
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            
            train_df,test_df = self.get_train_test_df()

            profile.calculate(train_df,test_df)

            # profile.json()
            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            with open(report_file_path, 'w') as report_file:
                json.dump(report, report_file, indent=6)

            return report 
        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir, exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self):
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()
            
            data_validation_arifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation performed Successfully.")

            logging.info(f"Data Validation Artifact: {data_validation_arifact}")
        except Exception as e:
            raise HousingException(e,sys) from e