import requests
from requests.auth import HTTPBasicAuth

url = 'http://{url}/api/v1/dags'

dags = requests.get(url, auth=HTTPBasicAuth('airflow', 'airflow')).json()
#is_active 만 하면 모든 DAG가 나오고 있기에 실제로 실행 한것중에는 is_paused가 False라 그것을 기준으로 변경하여 처리
print("Active DAGs:"+ str([dag['dag_id'] for dag in dags['dags'] if dag['is_paused'] == False]))