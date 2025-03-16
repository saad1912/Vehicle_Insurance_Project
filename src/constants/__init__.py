import os
from datetime import date

#For MongoDB connection
DATABASE_NAME = "Proj1"
COLLECTION_NAME = "Proj1-Data"
MONGODB_URL_KEY = "MONGODB_URL"

PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "Response"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJ_FILENAME = "preprocessing.pkl"

FILENAME : str = "Vehicle_Data.csv"
TRAIN_FILE_NAME : str = "train.csv"
TEST_FILE_NAME : str = "test.csv"
SCHEMA_FILE_PATH : str = os.path.join("config","schema.yaml")

AWS_ACCESS_KEY_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "us-east-1"



#Data Ingestion Related Constants
DATA_INGESTION_COLLECTION_NAME: str = "Proj1-Data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingestion"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25


#Data Validation related Constants
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME:str = "report.yaml"

