import uuid
import airflow
from airflow import DAG
from airflow.decorators import task
from airflow.operators.dummy import DummyOperator



with DAG(
    dag_id="Project_Mapping",
    start_date=airflow.utils.dates.days_ago(2),
    schedule_interval="@daily") as dag:

    start = DummyOperator(task_id="start")
    fetch_reddit_data = DummyOperator(task_id="Fetch_reddit_data")
    fetch_twitter_data = DummyOperator(task_id="Fetch_twitter_data")
    fetch_facebook_data = DummyOperator(task_id="Fetch_facebook_data")
    fetch_instagram_data = DummyOperator(task_id="Fetch_instagram_data")
    clean_reddit_data = DummyOperator(task_id="Clean_reddit_data")
    clean_twitter_data = DummyOperator(task_id="Clean_twitter_data")
    clean_facebook_data = DummyOperator(task_id="Clean_facebook_data")
    clean_instagram_data = DummyOperator(task_id="Clean_instagram_data")
    



    join_datasets = DummyOperator(task_id="Join_datasets")

    start >> [fetch_reddit_data, fetch_twitter_data, fetch_facebook_data, fetch_instagram_data]
    fetch_reddit_data >> clean_reddit_data
    fetch_twitter_data >> clean_twitter_data
    fetch_facebook_data >> clean_facebook_data
    fetch_instagram_data >> clean_instagram_data
    [clean_reddit_data, clean_twitter_data, clean_facebook_data, clean_instagram_data] >> join_datasets
    @task #task to train the model
    def train_model():
        model_id = "Hello"
        return model_id
    @task # task to deploy the model
    def deploy_model(model_id : str):
        
        return True

    model_id = train_model()
    deploy_model(model_id)

    join_datasets >> model_id