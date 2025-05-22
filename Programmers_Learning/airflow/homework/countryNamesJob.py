from airflow import DAG
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from datetime import datetime
from datetime import timedelta

import json
import requests
import logging
import psycopg2

def get_Redshift_connection(autocommit=True):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()


@task
def extract(url):
    logging.info("Extract started")
    f = requests.get(url)
    logging.info("Extract ended")
    return f.text

@task
def transform(text):
    logging.info("Transform started")
    records = []
    jsonArray = json.loads(text)
    for row in jsonArray:
        records.append([row['name']['official'].replace(""), row['area'], row['population']])
    logging.info("Transform ended")
    return records

@task
def initTable(dropYn=False):
    logging.info("initTable started")
    if dropYn:
        # 테이블이 있으면 삭제
        cur = get_Redshift_connection()
        cur.execute("DROP TABLE IF EXISTS azx4908.countryNames;")
        logging.info("Table dropped")
    cur = get_Redshift_connection()
    # 테이블이 없으면 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS azx4908.countryNames (
                official_name VARCHAR(100),
                area float,
                population INT)
    """)              

@task
def load(schema, records):
    logging.info("load started")    
    cur = get_Redshift_connection()   
    try:
        cur.execute("BEGIN;")
        cur.execute(f"DELETE FROM {schema}.countryNames;") 
        for r in records:
            name = r[0].replace("'", "''")  # SQL Injection 방지
            area = r[1]
            population = r[2]
            sql = f"INSERT INTO {schema}.countryNames VALUES ('{name}', '{area}','{population}');"
            logging.info(sql)
            cur.execute(sql)
        cur.execute("COMMIT;")   # cur.execute("END;") 
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        cur.execute("ROLLBACK;")   
        raise error
    logging.info("load done")


with DAG(
    dag_id='countryNamesJob',
    start_date=datetime(2025, 1, 1),  # 날짜가 미래인 경우 실행이 안됨
    schedule='30 6 * * 6',  # 적당히 조절
    max_active_runs=1,
    catchup=False,
    default_args={
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
) as dag:
    url = 'https://restcountries.com/v3/all' #
    schema = 'azx4908'

    lines = transform(extract(url))
    initTable(True)
    load(schema, lines)