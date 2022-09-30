# ETL aws

Welcome to this ETL project where we make used of postgres, docker, python and the most used cloud provider; aws.

To execute the ETL proccess in a property way we have to use a aws console account and create a S3 bucket with a aws user.

Please make sure to follow all the steps to succesfully be able to run this ETL.

## Create a S3 bucket into AWS.

Create a S3 bucket and call it as you want.

![buckets](https://user-images.githubusercontent.com/81943031/193343262-bc96aba1-436c-4211-b7cd-9d472d680cf3.png)

## Structure of S3 bucket

This is an important part, as I follow a specific folder structure in python scripts. Define the structure as follow:

<img width="1038" alt="bucket_folders" src="https://user-images.githubusercontent.com/81943031/193343844-2ce8647f-1512-4aa8-aa54-09676c2b9bbd.png">

After create the s3 bucket, upload into the folder "preprocess/" the csv file that is located in the root path "talks_info.csv". 

## S3 IAM user

In order to be able to interact with the S3 bucket, we have to create an user (or use an existing one).

<img width="1038" alt="new user" src="https://user-images.githubusercontent.com/81943031/193344008-976ea65d-e611-4b8a-8477-b62d8a40d455.png">

### Permissions for the user

Since we have many services and specific permissions to interact with them, we have to assign the S3 permission to the new user.

<img width="1008" alt="permission" src="https://user-images.githubusercontent.com/81943031/193344085-a6d6aacf-ab3d-4564-ac55-a7f782f86b40.png">

## Credentials

This is a very important step. You have to make sure of copy and save the credentials because we will use them later.

<img width="982" alt="credentials" src="https://user-images.githubusercontent.com/81943031/193344520-98a07a83-9ef9-4397-baa4-1cd55c6950a2.png">
 
## Create .env file

To use credentials, which are sensitive information, create an .env file with the following env variables. 

pdt: Do not share credentials with anyone.

![Screen Shot 2022-09-30 at 2 43 19 PM](https://user-images.githubusercontent.com/81943031/193345216-67e3e036-e973-4d35-a22c-e4f0e896e36c.png)

## Postgres database.

To proceed with the rest of the steps, make sure of have docker and docker compose installed in your machine.

Also make sure to be in the etl-aws folder (root folder), and run the following command.

__docker compose up__

It will create a docker container with a postgres database. 

These are the values of the user created.

<img width="241" alt="Screen Shot 2022-09-30 at 2 50 42 PM" src="https://user-images.githubusercontent.com/81943031/193346089-49ba43bd-4338-473d-988a-f5160843d9a9.png">

You can use adminer to interact with the webserver and manage from there the postgres database.

enter to the following url:

http://localhost:8080

<img width="685" alt="Screen Shot 2022-09-30 at 2 54 17 PM" src="https://user-images.githubusercontent.com/81943031/193346589-33de5a2a-5cbe-401e-82f7-78a7b6279cd4.png">

## Install required dependencies

To install dependencies, just run the following command:

pd: make sure to be in the root_folder (etl-aws)

__pip install -r requirements.txt__


## Run the ETL

To run the ETL process just run:

__python3 main.py__

It will extract the talks_info.csv which is located into the S3 bucket and save it into __data/preprocess__, then,
it will transform data and save into the path __data/staging__, later, it will save data into a postgres database and into the s3 bucket
in the following path: __staging/__.
