import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.proj1 import Proj1

from src.logger import logging
from src.exception import MyException

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e,sys)
        
    def export_data_into_feature_store(self)->DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from mongodb to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Loading Data from MongoDB....")
            proj1 = Proj1()
            df = proj1.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info("Data Loaded from MongoDB!!!!")
            logging.info(f"Shape of dataframe: {df.shape}")
            feature_store_filepath = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_filepath)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving Exported data into the feature store file path : {feature_store_filepath}")
            df.to_csv(feature_store_filepath, index=False, header=True)
            return df
        except Exception as e:
            raise MyException(e,sys) from e
    
    def split_data_as_train_test(self, df:DataFrame)-> None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")
        try:
            train, test = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed Train Test Split...")
            training_file_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            testing_file_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(training_file_path, exist_ok=True)
            os.makedirs(testing_file_path,exist_ok=True)
            logging.info("Exporting Train and Test Data..")
            train.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Successfully Exported!!!!!!")
        except Exception as e:
           raise MyException(e, sys) from e
    
    
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try: 
            
            df = self.export_data_into_feature_store()
            logging.info("Data Exported to Feature Store")
            self.split_data_as_train_test(df)
            logging.info("Train and Test data exported to respective filepaths")
            
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data Ingestion Artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        
        