from charts.models import NoticeInfo
import re

de_tech = [
    "Python","SQL","Java","Scala","Bash", "Trino", "Keras", "LLM", "ArgoCD", "Hudi", "Iceberg", "Kotlin", "Databricks", "MSK", "Shell Scripting","Tensorflow", "Pytorch", "Excel", "Tableau","R","Go","RDBMS","PostgreSQL","MySQL","Oracle","SQL Server","SQLite","MariaDB","NoSQL","MongoDB","Cassandra","Redis","HBase","Couchbase","DynamoDB","Cosmos DB","Data Warehouse","Redshift","BigQuery","Snowflake","Synapse Analytics","Teradata","Vertica","Hive","Data Lake","S3","GCS","HDFS","Spark","PySpark","Spark Streaming","kafka", "Flink","MapReduce","Pig","NiFi","StreamSets","Stitch","Fivetran","Matillion","Talend","Informatica","DataStage","Glue","Azure","GCP","dbt","CDC","Debezium","Striim","Kafka","Airflow","Luigi","Azkaban","AWS","GCP","EC2","RDS","EMR","Datahub","Redash", "Superset","Kinesis","VPC","IAM","HDInsight","Data Modeling","Data Governance","Alation", "Collibra", "Apache Atlas", "Hadoop", "YARN", "ZooKeeper", "Avro", "Parquet", "CI/CD","Jenkins","CircleCI","Docker","Kubernetes","ECS", "EKS", "AKS", "GKE", "Prometheus","Grafana","ELK", "Elasticsearch","Logstash","Athena","Kibana","CloudWatch","Datadog", "Splunk", "Monitoring","Terraform","Pulumi", "Ansible", "API", "REST","Git", "MLOps"
]

def preprocess(text):
    # 영단어와 한글 조사 분리: "Hadoop과" → "Hadoop 과"
    text = re.sub(r'([a-zA-Z]+)(?=[가-힣])', r'\1 ', text)
    # 특수문자 제거 후 소문자로 변환
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return text

def find_tech(text, techlist):
    find_text = preprocess(text)
    find_text_set = set(find_text.split())
    rtn_list = set()

    for item in techlist:
        if item.lower() in find_text_set:
            rtn_list.add(item)

    return list(rtn_list)

def dedupe_case_insensitive(input_set):
    temp = {}
    for item in input_set:
        key = item.lower()
        if key not in temp:
            temp[key] = item
    return set(temp.values())

def transform_to_techstack():
    notices = NoticeInfo.objects.all()
    
    update_notice_list = []
    
    for notice in notices:
        # print(f'notice.notice_title : {notice.notice_title}')
        # print(f'notice.notice_position : {notice.notice_position}')
        # print(f'notice.notice_main_work : {notice.notice_main_work}')
        # print(f'notice.notice_qualification : {notice.notice_qualification}')
        # print(f'notice.notice_preferred_qualification : {notice.notice_preferred_qualification}')
        # print(f'notice.notice_tech_stack : {notice.notice_tech_stack}')
        
        tech_set = set()
        
        tech_set.update(find_tech(notice.notice_position, de_tech))
        tech_set.update(find_tech(notice.notice_main_work, de_tech))
        tech_set.update(find_tech(notice.notice_qualification, de_tech))
        tech_set.update(find_tech(notice.notice_preferred_qualification, de_tech))
        
        if notice.notice_tech_stack:
            tech_set.update(notice.notice_tech_stack.split('\n'))
        
        result_set = dedupe_case_insensitive(tech_set)
        notice.notice_tech_stack = '\n'.join(result_set)
        
        update_notice_list.append(notice)
    
    NoticeInfo.objects.bulk_update(update_notice_list, ['notice_tech_stack'])
