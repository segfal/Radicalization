import os

## get month and year
import datetime
month = datetime.datetime.now().strftime("%m")
year = datetime.datetime.now().strftime("%Y")

import boto3


import dotenv

dotenv.load_dotenv()

## load aws credentials
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_password = os.getenv("AWS_PASSWORD")
aws_name = os.getenv("AWS_NAME")

s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-1'
)

bucket = s3.Bucket(aws_name)





for i in range(0,30):
    ## get the file name
    filename = "reddit_posts_" + str(year) + "-" + str(month) + "-" + str(i) + ".xlsx"
    ## check if file exists
    if os.path.isfile(filename):

        ## upload file to s3
        s3.meta.client.upload_file(filename, aws_name, filename)
        print(filename)
        ## delete the file
        os.remove(filename)
        print("Deleted file: " + filename)
    else:
        continue






