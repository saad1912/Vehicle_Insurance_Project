import sys
from src.entity.config_entity import VehiclePredictorConfig
from src.entity.s3_estimator import Proj1Estimator
from src.exception import MyException
from src.logger import logging
import pandas as pd

class VehicleData:

    def __init__(self, 
                 Gender,
                 Age,
                 Driving_License,
                 Region_Code,
                 Previously_Insured,
                 Annual_Premium,
                 Policy_Sales_Channel,
                 Vintage,
                 Vehicle_Age_lt_1_Year,
                 Vehicle_Age_gt_2_Years,
                 Vehicle_Damage_Yes):
        try:

            self.Gender = Gender
            self.Age = Age
            self.Driving_License = Driving_License
            self.Region_Code  = Region_Code
            self.Previously_Insured = Previously_Insured
            self.Annual_Premium = Annual_Premium
            self.Policy_Sales_Channel  = Policy_Sales_Channel
            self.Vintage = Vintage
            self.Vehicle_Age_lt_1_Year = Vehicle_Age_lt_1_Year
            self.Vehicle_Age_gt_1_Years = Vehicle_Age_gt_2_Years
            self.Vehicle_Damage_Yes = Vehicle_Damage_Yes
        except Exception as e:
            raise MyException (e,sys) from e

    def get_vehicle_input_as_dict(self):

        logging.info("Entered get_vehicle_input_as_dict function...")
        try:

            input_data = {
                "Gender" : [self.Gender],
                "Age" : [self.Age],
                "Driving_License" : [self.Driving_License],
                "Region_Code":[self.Region_Code],
                "Previously_Insured":[self.Previously_Insured],
                "Annual_Premium" : [self.Annual_Premium],
                "Policy_Sales_Channel":[self.Policy_Sales_Channel],
                "Vintage" : [self.Vintage],
                "Vehicle_Age_lt_1_Year":[self.Vehicle_Age_lt_1_Year],
                "Vehicle_Age_gt_2_Years":[self.Vehicle_Age_gt_1_Years],
                "Vehicle_Damage_Yes":[self.Vehicle_Damage_Yes]
            }
            return input_data
        except Exception as e:
            raise MyException(e,sys) from e
        
    def get_vehicle_data_as_dataframe(self):
        
        logging.info("Entered get_vehicle_input_as_dataframe function...")
        try:
            vehicle_data_dict = self.get_vehicle_input_as_dict()
            logging.info("Successfully return single-row dataframe for prediction!!!!")
            return pd.DataFrame(vehicle_data_dict)

        except Exception as e:
            raise MyException(e,sys) from e
        


class VehicleDataClassifier:
    def __init__(self, prediction_pipeline_config:VehiclePredictorConfig=VehiclePredictorConfig()):
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise MyException(e,sys) from e
    
    def predict(self,dataframe:pd.DataFrame):

        logging.info("Entered the predict function of VehicleDataClassifier...")
        try:
            model = Proj1Estimator(
                model_path=self.prediction_pipeline_config.model_file_path,
                bucket_name=self.prediction_pipeline_config.model_bucket_name
            )
            result = model.predict(dataframe)
            return result
        except Exception as e:
            raise MyException(e,sys) from e
        