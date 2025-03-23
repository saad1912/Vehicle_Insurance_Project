import os
import sys
from src.logger import logging
from src.exception import MyException

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation

from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Entered Data Ingestion part of TrainPipeline>>>>>>>>")
            logging.info("Getting the data from MongoDB..")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from MongoDB!!")
            logging.info(">>>>>>>>>>Exiting Data Ingestion part of TrainPipeline")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys) from e
    
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)-> DataValidationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data validation component
        """
        try:
            logging.info("Entered Data Validation part of TrainPipeline>>>>>>>>")
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact,
                                            data_validation_config = self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the Data Validation Operation!!!")
            logging.info(">>>>>>>>>>Exiting Data Validation part of TrainPipeline")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys) from e

    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_artifact:DataValidationArtifact)-> DataTransformationArtifact:
        try : 
            logging.info("Entered Data Transformation part of TrainPipeline>>>>>>>>")
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                    data_validation_artifact=data_validation_artifact,
                                                    data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Performed the Data Tranformation Operation!!!")
            logging.info(">>>>>>>>>>Exiting Data Transformation part of TrainPipeline")
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        
    
    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact)-> ModelTrainerArtifact:
        try : 
            logging.info("Entered Model Trainer part of TrainPipeline>>>>>>>>")
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                                    model_trainer_config=self.model_trainer_config)
            model_trainer_artifact = model_trainer.initialize_model_trainer()
            logging.info("Performed the Model Trainer Operation!!!")
            logging.info(">>>>>>>>>>Exiting Model Trainer part of TrainPipeline")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys) from e
    
    def start_model_evaluation(self, data_ingestion_artifact:DataIngestionArtifact,
                               model_trainer_artifact : ModelTrainerArtifact)-> ModelEvaluationArtifact:
        try : 
            logging.info("Entered Model Trainer part of TrainPipeline>>>>>>>>")
            model_evaluation = ModelEvaluation(model_eval_config=self.model_evaluation_config,
                                               model_trainer_artifact=model_trainer_artifact,
                                               data_ingestion_artifact=data_ingestion_artifact)
            model_evaluation_artifact = model_evaluation.initialize_model_evaluation()
            logging.info("Performed the Model Evaluation Operation!!!")
            logging.info(">>>>>>>>>>Exiting Model Evaluation part of TrainPipeline")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        
        


    def run_pipeline(self)-> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                          data_validation_artifact=data_validation_artifact,
                                                                          )
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,model_trainer_artifact=model_trainer_artifact)
        except Exception as e:
            raise MyException(e,sys) from e
        