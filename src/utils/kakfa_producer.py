'''
    Author: Kyle Ong
    Date: 02/18/19

    Kafka producer for trenddit

    downloads data from s3
    publishes them to a kafka topic
'''
from confluent_kafka import Producer
import boto3

s3 = boto3.resource('s3')
p = Producer({
    'bootstrap.servers': 'localhost:9092'
})

BUCKET_NAME = "enter your bucket name"
key = "enter your key name"

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def main():
    for data in s3.Object(BUCKET_NAME, key).get(Range = "0-1")["Body"].iter_lines():
        p.poll(0)
        p.produce('persons-avro', data.encode('utf-8'), callback=delivery_report)

    p.flush()



if __name__ == "__main__":
    main()
