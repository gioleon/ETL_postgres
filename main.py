from s3_extract import get_file
from transform import main_transform, save_data_db
from load_s3 import load_data
from db_operations import create_table


if __name__ == "__main__":
    
    # Download file from S3 bucket
    get_file()

    # Transform data. main function returs a new DataFrame
    new_df = main_transform()
    
    # Create table
    create_table()

    #Save data into the created table
    save_data_db(new_df)

    # Load data to S3 bucket
    load_data()

