# Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Run Instructions](README.md#run-instructions)
4. [Test Instructions](README.md#test-instructions)


# Problem

Reddit generates ~2 million comments / day. 480,000 of those comments are banned / flagged as inapropriate. The rules for banning / flagging comments are rule or regex based. They are inefficient.

Social Media companies take platform abuse seriously.

This project aims to automate the process of collecting the necessary data to run in depth analysis on reddit comments. Latent Diriclecht Allocation is used to extract topics from a corpus of reddit comments. A neural network is trained on these topics of intent. A data pipeline ingests reddit data to classify reddit comments by intent in real-time.

# Approach
```
      ├── README.md 
      ├── pom.xml
      ├── src
      │   ├── dash_end
      │   │     └──app.py
      │   │     └──constants.py
      │   │     └──requirements.txt
      │   ├── main
      │   │     └──Constants.scala
      │   │     └──sink.scala
      │   ├── utils
      │         └──kafka_producer.py
```
h1b_counting.py is the entry-point of the program. A DataProcessor object is initialized and aggregates statstics from input files line-by-line. After all files have been processed write the statistics to a txt file.
DataProcessor draws inspiration from a pandas DataFrame.
 

# Run-Instructions
## Clone the Repo
```
    cd /desired/location
    git clone https://github.com/kho226/reddit-comment-classifier/
```
## Install Confluent
```
    cd
    curl -O http://packages.confluent.io/archive/5.1/confluent-5.1.0-2.11.zip
    unzip confluent confluent-5.1.0-2.11.zip
```
## Start services
```
    cd confluent-5.1.0-2.11
    bin/zookeeper-server-start etc/kafka/zookeeper.properties
    bin/kafka-server-start etc/kafka/server.properties
    bin/schema-registry-start etc/schema-registry/schema-registry.properties
```

## Register schema
```
    cd /location/of/reddit-comment-classifier/src/main/resources/register_schema.py
    python register_schema.py http://localhost:8081 persons-avro person.avsc
    curl http://localhost:8081/subjects/persons-avro-value/versions/1
```

## Install Gradle
```
    brew install gradle
```

## Build Jars
```
    cd /location/of/reddit-comment-classifier
    gradle init
    ./gradlew build
```

## Run Jars
```
    java -jar build/libs/utils.jar
```

## Start Consumer
```
    cd
    cd /location/of/confluent-5.1.0-2.11
    bin/kakfa-console-avro-consumer --bootstrap-server localhost:9092 --topic avro-persons
```

## Download / install  Maven
```
    wget https://www-eu.apache.org/dist/maven/maven-3/3.6.0/binaries/apache-maven-3.6.0-bin.zip
    unzip apache-maven-3.6.0-bin.zip
    sudo echo "/path/to/apache-maven-3.6.0/bin" >> /etc/paths
    mvn -v
```

## Build / run spark job
```
    cd reddit-comment-classifier
    mvn package
    spark-submit --class proj.StreamProcessor --master local[4] /location/of/proj_0.0.1-0.0.1-jar-with-dependencies.jar
```




# Test-Instructions

```
    tbd
```

