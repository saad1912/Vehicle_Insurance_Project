from src.exception import MyException
from src.logger import logging
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import DataIngestionArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from src.entity.s3_estimator import Proj1Estimator
from typing import Optional
from sklearn.metrics import f1_score
from src.utils.main_utils import load_object
from src.constants import TARGET_COLUMN

import sys
import pandas as pd

from src.entity.s3_estimator import Proj1Estimator
from dataclasses import dataclass

@dataclass
class EvaluateModelResponse:
    trained_model_f1_score:float
    best_model_f1_score:float
    is_model_accepted:bool
    difference:float



class ModelEvaluation:

    def __init__(self, model_eval_config:ModelEvaluationConfig,data_ingestion_artifact:DataIngestionArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys) from e
    

    def get_best_model(self)-> Optional[Proj1Estimator]:
        """
        Method Name :   get_best_model
        Description :   This function is used to get model from production stage.
        
        Output      :   Returns model object if available in s3 storage
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.s3_model_key_path
            proj1estimator = Proj1Estimator(bucket_name=bucket_name,model_path=model_path)
            if proj1estimator.is_model_present(model_path=model_path):
                return proj1estimator
            return None
        except Exception as e:
            raise MyException(e,sys)
    
    def _map_gender_column(self,df):
        """Map Gender column to 0 for Female and 1 for Male."""
        df['Gender'] = df['Gender'].map({'Male':1,'Female':0}).astype(int)
        return df
    
    def _create_dummy_columns(self,df):
        """Create dummy variables for categorical features."""

        categorical_columns = df.select_dtypes(include=['object']).columns
        # Filter out high-cardinality columns (e.g., those with >= 50 unique values)
        threshold = 50
        columns_to_encode = [col for col in categorical_columns if df[col].nunique() < threshold]
        logging.info(f"Columns selected for dummy encoding: {columns_to_encode}")
        df = pd.get_dummies(df, columns=columns_to_encode, drop_first=True)
        return df
    
    def _rename_columns(self, df):
        """Rename specific columns and ensure integer types for dummy columns."""
        logging.info("Renaming specific columns and casting to int")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })
        for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col] = df[col].astype('int')
        return df
    
    def _drop_id_column(self,df):
        """Drop the 'id' column if it exists."""
        logging.info("Dropping 'id' column")
        if "_id" in df.columns:
            df = df.drop("_id", axis=1)
        return df

    

    def evaluate_model(self)->EvaluateModelResponse:
        """
        Method Name :   evaluate_model
        Description :   This function is used to evaluate trained model 
                        with production model and choose best model 
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try: 

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            x,y = test_df.drop(TARGET_COLUMN),test_df[TARGET_COLUMN]

            x = self._map_gender_column(x)
            x = self._create_dummy_columns(x)
            x = self._drop_id_column(x)
            x = self._rename_columns(x)

            trained_model = load_object(self.model_trainer_artifact.trained_model_file_path)
            logging.info("Trained model loaded...")
            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            logging.info(f"F1 score of this model is {trained_model_f1_score}")

            
            best_model_f1_score = None
            best_model = self.get_best_model()

            if best_model is not None:
                y_pred_best_model = best_model.predict(x)
                logging.info("Computing F1 score of production model")
                best_model_f1_score = f1_score(y_pred_best_model,y)
                logging.info(f"F1 score of production model is {best_model_f1_score}")

            
            tmp_best_model_score = 0 if best_model_f1_score is None else best_model_f1_score

            result = EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=tmp_best_model_score
                is_model_accepted=(trained_model_f1_score>tmp_best_model_score)
                difference= trained_model_f1_score - tmp_best_model_score
            )
            logging.info(f"Result-> {result}")
        
        except Exception as e:
            raise MyException(e,sys) from e
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:

        try:
            print("------------------------------------------------------------------------------------------------")
            logging.info("Initialized Model Evaluation Component.")
            evaluate_model_response = self.evaluate_model()
            s3_model_path = self.model_eval_config.s3_model_key_path

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                changed_accuracy=evaluate_model_response.difference
                s3_model_path=s3_model_path,
                trained_model_path=self.model_trainer_artifct.trained_model_file_path
            )
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact

        except Exception as e:
            raise MyException(e,sys) from e
        

        


