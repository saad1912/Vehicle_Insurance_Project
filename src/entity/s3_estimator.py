from src.cloud_storage.aws_storage import SimpleStorageService
from src.entity.estimator import MyModel
from src.exception import MyException
from src.logger import logging
from pandas import DataFrame
import sys



class Proj1Estimator:
    """
    This class is used to save and retrieve our model from s3 bucket and to do prediction
    """

    def __init__(self, bucket_name,model_path):
        self.bucket_name = bucket_name
        self.model_path = model_path
        self.loaded_model:MyModel=None
        self.s3 = SimpleStorageService()
    
    def is_model_present(self,model_path):
        """
        Check whether the model is present or not at S3 location
        """
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name,s3_key=model_path)
        except Exception as e:
            raise MyException(e,sys) from e
    
    def load_model(self,)->MyModel:
        """
        Load the model from the model_path
        :return:
        """
        try:
            return self.s3.load_model(self.model_path,bucket_name=self.bucket_name)
        except Exception as e:
            raise MyException(e,sys) from e
    
    def save_model(self, from_filename,remove:bool=False):
        """
        Save the model to the model_path
        :param from_file: Your local system model path
        :param remove: By default it is false that mean you will have your model locally available in your system folder
        :return:
        """
        try:
            return self.s3.upload_file(from_filename,self.model_path,self.bucket_name,remove=remove)
        except Exception as e:
            raise MyException(e,sys) from e
        
    def predict(self, dataframe:DataFrame):
        """
        :param dataframe:
        :return:
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe)
            
        except Exception as e:
            raise MyException(e,sys) from e
