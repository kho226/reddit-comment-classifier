# Table of Contents
1. [Problem](README.md#problem)
2. [Architecture] (README.md#architecture)
2. [Approach](README.md#approach)
3. [Run Instructions](README.md#run-instructions)
4. [Test Instructions](README.md#test-instructions)


# Problem

Reddit generates ~2 million comments / day. 480,000 of those comments are banned / flagged as inapropriate. The rules for banning / flagging comments are rule or regex based. They are inefficient.

Imagine you are a data scientist or platform moderator looking to analyze a large body of text. This entails finding a dataset, cleaning it, and dumping it into a datastore. Then after building your query, your results are totally irrelevant to your initial question.

This project aims to lower the barrier to entry for in-depth analysis over a large body of text. Trenditt is a real-time streaming platform that enables realtime analysis over a large body of text.

# Architecture
![alt text] (https://raw.githubusercontent.com/kho226/trenddit/dash_end/Screen\ Shot\ 2019-03-18\ at\ 3.35.07\ PM.png)

# Approach
```
      ├── README.md 
      ├── pom.xml
      ├── src
      │   ├── main
      │   │     ├── scala
      │   │     │      └──sink.scala
      │   │     │      └──Constants.scala
      │   │     │      └──MLSink.scala
      │   │     │      └──RandomForestModel.scala
      │   │     ├── resources
      │   │     │      └──application.conf
      │   │     │      └──log4j.properties
      │   ├──frontend 
      │   │     └── app.py
      │   │     └── constants.py
      │   │     └── requirements.txt       
      │   ├──utils 
      │   │     └── kafka_producer.py       
```
kafka_producer.py will download byte sized chunks of data from s3 and publish them to a kafka topic.
sink.scala subsrcibes to this topic.
Incoming messages are classified by RandomForest.scala.
Classified messages are written to elasticsearch by sink.scala.
app.py queries elasticsearch and caches frequently used queries in redis.
 
# Dependencies
- elasticsearch 6.5.2
- spark 2.2.1
- hadoop 2.7
- redis 5.0.3
- python 2.7
- dash 0.36.0

# Run-Instructions
## Clone the Repo
```
    cd /desired/location
    git clone https://github.com/kho226/trenddit
```
## Install elasticsearch (https://www.elastic.co/guide/en/elasticsearch/reference/6.5/zip-targz.html)
```
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.5.2.zip
    unzip elasticsearch-6.5.2.zip
```
## Install elasticsearch discovery-ec2 (https://www.elastic.co/guide/en/elasticsearch/plugins/6.5/discovery-ec2.html)
```
   elasticsearch-6.5.2/bin/elastisearch-plugin install discovery-ec2
   elasticsearch-6.5.2/bin/elasticsearch-keystore create
   elasticsearch-6.5.2/bin/elasticsearch-keystore add discovery.ec2.access_key
   elasticsearch-6.5.2/bin/elasticsearch-keystore add discovery.ec2.secret_key
   
```
## Start elasticsearch
```
    elasticsearch-6.5.2/bin/elasticsearch
```
## Install Redis
```
    wget http://download.redis.io/releases/redis-5.0.3.tar.gz
    tar xzf redis-5.0.3.tar.gz
    cd redis-5.0.3
    make
```
## Start Redis
```
    src/redis-server
```
## Install Spark
```
    wget https://archive.apache.org/dist/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz
    tar xvf spark-2.2.1-bin-hadoop2.7.tgz
```
## Setup virtualenv for dash
```
    cd trenddit/front_end
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
```
## run dash app
```
    (venv) python app.py
```
## Install Confluent
```
    cd
    curl -O http://packages.confluent.io/archive/5.1/confluent-5.1.0-2.11.zip
    unzip confluent confluent-5.1.0-2.11.zip
```
## Start Confluent services
```
    cd confluent-5.1.0-2.11
    bin/zookeeper-server-start etc/kafka/zookeeper.properties
    bin/kafka-server-start etc/kafka/server.properties
    bin/schema-registry-start etc/schema-registry/schema-registry.properties
```
## Install SDK man
```
    curl -s "https://get.sdkman.io" | bash
```
## Install maven
```
    sudo apt install maven
```
## Install confluent-kafka / boto3
```
    pip install confluent-kafka
    pip install boto3
```
## Start kafka_producer
```
    cd trenddit/utils
    python kafka_producer.py
```
## Build / run spark job
```
    cd trenddit
    mvn package
    spark-submit --master local[*] /location/of/trenddit_0.0.1-0.0.1-jar-with-dependencies.jar
```