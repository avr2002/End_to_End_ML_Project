from housing.pipeline.pipeline import Pipeline
from housing.logger import logging
from housing.config.configuration import Configuration
# from housing.component.data_transformation import DataTransformation
from housing.util.util import load_data

def main():
    try:
        # data_validation_config = Configuration().get_data_validation_config()
        # print(data_validation_config)

        # schema_file_path = r"C:\Users\Amit Vikram Raj\#FSDS_iNeuron\03.Machine Learning\End_to_End_ML_Project\config\schema.yaml"
        # file_path = r"C:\Users\Amit Vikram Raj\#FSDS_iNeuron\03.Machine Learning\End_to_End_ML_Project\housing\artifact\data_ingestion\2022-09-20-13-11-02\ingested_data\train\housing.csv"

        # df = load_data(file_path=file_path, schema_file_path=schema_file_path)
        # print(df.columns)
        # print(df.dtypes)

        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)


if __name__=="__main__":
    main()