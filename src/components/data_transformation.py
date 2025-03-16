import os
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTEENN
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.constants import *
from src.utils.main_utils import read_yaml_file, save_object,save_numpy_array_data


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config
        self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

    @staticmethod
    def read_data(file_path: str) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)

    def get_transformer_object(self) -> Pipeline:
        logging.info("Entering get_transformer_object function....")
        try:
            standard_scaler = StandardScaler()
            minmax_scaler = MinMaxScaler()
            logging.info("Standard Scaler and Min Max objects initialized")
            standard_scaler_columns = self._schema_config['num_features']
            minmax_scaler_columns = self._schema_config['mm_columns']
            logging.info("Standard Scaler and Min Max columns saved in variables")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("Standard Scaler", standard_scaler, standard_scaler_columns),
                    ("MinMax Scaler", minmax_scaler, minmax_scaler_columns)
                ],
                remainder="passthrough"
            )
            logging.info("Column Transformer initialized")
            final_pipeline = Pipeline(steps=[("Preprocessor", preprocessor)])
            logging.info("Final Pipeline ready!!!!!!!!!")
            logging.info("Exiting get_transformer_object function.....")
            return final_pipeline
        except Exception as e:
            logging.info("Exception occurred in get_transformer_object function")
            raise MyException(e, sys) from e

    def _map_gender_column(self, df):
        logging.info("Mapping Gender column: Female=0, Male=1")
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
        return df

    def _create_dummy_columns(self, df):
        logging.info("Creating dummy variables for categorical columns")
        # Select only object type columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        # Filter out high-cardinality columns (e.g., those with >= 50 unique values)
        threshold = 50
        columns_to_encode = [col for col in categorical_columns if df[col].nunique() < threshold]
        logging.info(f"Columns selected for dummy encoding: {columns_to_encode}")
        return pd.get_dummies(df, columns=columns_to_encode, drop_first=True)

    def _rename_columns(self, df):
        logging.info("Renaming specific columns")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })
        for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col] = df[col].astype(int)
        return df

    def _drop_columns(self, df):
        logging.info("Dropping extra columns")
        drop_columns = self._schema_config['drop_columns']
        return df.drop(columns=drop_columns, axis=1)

    def initiate_data_transformation(self):
        try:
            logging.info("Data Transformation Initiated")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)

            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)
            logging.info("Train-Test data loaded")

            train_input_feature = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            train_target_feature = train_df[TARGET_COLUMN]
            logging.info("Train features and target created")

            test_input_feature = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            test_target_feature = test_df[TARGET_COLUMN]
            logging.info("Test features and target created")

            logging.info("Starting Data Preprocessing")
            train_input_feature = self._map_gender_column(train_input_feature)
            train_input_feature = self._create_dummy_columns(train_input_feature)
            train_input_feature = self._rename_columns(train_input_feature)
            train_input_feature = self._drop_columns(train_input_feature)

            test_input_feature = self._map_gender_column(test_input_feature)
            test_input_feature = self._create_dummy_columns(test_input_feature)
            test_input_feature = self._rename_columns(test_input_feature)
            test_input_feature = self._drop_columns(test_input_feature)
            logging.info("Data Preprocessing completed")

            logging.info("Creating transformer object")
            preprocessor = self.get_transformer_object()
            logging.info("Transformer object obtained")

            train_input_feature = preprocessor.fit_transform(train_input_feature)
            test_input_feature = preprocessor.fit_transform(test_input_feature)
            logging.info("Data Transformation completed")

            logging.info("Applying SMOTEENN for imbalanced dataset")
            smt = SMOTEENN(sampling_strategy="minority")
            train_input_feature, train_target_feature = smt.fit_resample(train_input_feature, train_target_feature)
            test_input_feature, test_target_feature = smt.fit_resample(test_input_feature, test_target_feature)
            logging.info("SMOTEENN applied")

            train_arr = np.c_[train_input_feature, np.array(train_target_feature)]
            test_arr = np.c_[test_input_feature, np.array(test_target_feature)]
            logging.info("Concatenated features and targets")

            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            logging.info("Transformed objects and files saved")

            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
        except Exception as e:
            raise MyException(e, sys) from e
