import uuid
import airflow
from airflow import DAG
from airflow.decorators import task
from airflow.operators.dummy import DummyOperator
#import pull_data as pull
#import pgresload as pgres
#import train_data as train
#import loadtopgres as load
#import reddit_data as reddit
#import s3

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator



'''


with DAG(
    dag_id="Project_Mapping",
    start_date=airflow.utils.dates.days_ago(2),
    schedule_interval="@hourly") as dag:
    ##data from reddit
  

    

   



    @task
    def get_reddit_data():
        import reddit_data as reddit
        redditdata = reddit.Reddit()
        redditdata.push_to_excel('doomer',10)
      
    
    @task
    def loading_data():
        import reddit_data as reddit
        redditdata = reddit.Reddit()
        redditdata.load_data()
    
    

    @task
    def load_to_s3():
        import reddit_data as reddit
        redditdata = reddit.Reddit()
        redditdata.push_to_s3()


    
    start = get_reddit_data()
    
    loading = loading_data()
    finish = load_to_s3()


    start >> loading >> finish


    '''



dag = DAG(
    dag_id="Project_Mapping",
    start_date=airflow.utils.dates.days_ago(2),
    schedule_interval=None)


def _get_reddit_data():
    import reddit_data as reddit
    redditdata = reddit.Reddit()
    redditdata.push_to_excel('doomer',10)
    
def _loading_data():
    import reddit_data as reddit
    redditdata = reddit.Reddit()
    redditdata.load_data()

def _load_to_s3():
    import reddit_data as reddit
    redditdata = reddit.Reddit()
    redditdata.push_to_s3()

##First Task
get_reddit_data = PythonOperator(
    task_id="get_reddit_data",
    python_callable=_get_reddit_data,
    dag=dag)



loading_data = PythonOperator(
    task_id="loading_data",
    python_callable=_loading_data,
    dag=dag)


load_to_s3 = PythonOperator(
    task_id="load_to_s3",
    python_callable=_load_to_s3,
    dag=dag)


##First Task
get_reddit_data >> loading_data >> load_to_s3

