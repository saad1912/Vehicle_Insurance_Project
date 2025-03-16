import sys
from typing import Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.exception import MyException
from src.logger import logging

from src.utils.main_utils import save_object,load_numpy_array_data,load_object
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact,ClassificationMetricArtifact,ModelTrainerArtifact
from src.entity.estimator import MyModel

class ModelTrainer:
    def __init__(self, data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train:np.array, test:np.array)-> Tuple[object,object]:
        """
        Method Name :   get_model_object_and_report
        Description :   This function trains a RandomForestClassifier with specified parameters
        
        Output      :   Returns metric artifact object and trained model object
        On Failure  :   Write an exception log and then raise an exception
        """
        try: 

            logging.info("Entered get_model_object_and_report function..")
            X_train,y_train,X_test,y_test = train[:,:-1], train[:,-1], test[:,:-1], test[:,-1]
            logging.info("Train-Test split done..")
            model = RandomForestClassifier(
                n_estimators=self.model_trainer_config._n_estimators,
                max_depth=self.model_trainer_config._max_depth,
                min_samples_leaf=self.model_trainer_config._min_samples_leaf,
                min_samples_split=self.model_trainer_config._min_samples_split,
                criterion=self.model_trainer_config._criterion,
                random_state=self.model_trainer_config._random_state
            )
            logging.info("Model defined..")


            logging.info("Fitting the model...")
            model.fit(X_train,y_train)
            logging.info("Model is fitted successfully..")

            y_pred = model.predict(X_test)
            f1 = f1_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)

            metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision=precision, recall=recall)
            return model, metric_artifact
        except Exception as e:
            raise MyException(e,sys) from e
    
    def initialize_model_trainer(self)-> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates the model training steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try : 
            print("Starting Model Trainer Component")
            train_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            logging.info("Train-Test data loaded")

            trained_model, metric_artifact = self.get_model_object_and_report(train_arr,test_arr)
            logging.info("Model object and artifact loaded")

            preprocessing_obj = load_object(self.data_transformation_artifact.transformed_object_file_path)
            logging.info("Preprocessing Object Loaded")

            if accuracy_score(trained_model.predict(train_arr[:,:-1]), train_arr[:,-1])<self.model_trainer_config.expected_accuracy:
                logging.info("Chosen Model doesn't beat baseline score")
                raise Exception("Chosen Model doesn't beat baseline score")

            mymodel = MyModel(preprocessing_obj=preprocessing_obj,trained_model_object=trained_model)
            logging.info("Preprocessing Object and Trained Model wrapped")

            save_object(self.model_trainer_config.trained_model_file_path,mymodel)
            logging.info("Saved wrapper model having preprocessor object and training model")

            # Create and return the ModelTrainerArtifact
            model_trainer_artifact = ModelTrainerArtifact(
                    trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                    metric_artifact=metric_artifact,
                )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        
    
