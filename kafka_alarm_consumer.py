from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from Entities.Alarm import Alarm
from datetime import datetime

import py_eureka_client.eureka_client as eureka_client

eureka_client.init(eureka_server="http://localhost:8761/eureka",
                   app_name="front-end-service",
                   instance_port=5000)


bootstrap_server, consumer_topic, producer_topic = \
    map(str.strip, open('bootstrapservers.txt', 'r').read().split(','))

Base = declarative_base()
engine = create_engine('sqlite:///alarms.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


consumer = KafkaConsumer(
    consumer_topic,
    bootstrap_servers=[bootstrap_server],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='cli',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=[bootstrap_server],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)


while True:
    session = Session()

    data = consumer.poll(timeout_ms=100)

    for _, messages in data.items():
        print(type(messages))
        for message in messages:
            print(type(message))
            try:
                value = message.value
                sent = datetime.fromtimestamp(value['timestamp'])
                received = datetime.now()
                elapsed = (received - sent).total_seconds()

                alarm = Alarm(value['facilityId'], value['sensorId'], elapsed, 1)
                alarm_json = dumps(alarm.__repr__())
                producer.send(producer_topic, value=alarm_json)
                print(alarm.__repr__() + " persisted and published")

            except ValueError as e:
                print(e)
            try:
                session.merge(alarm)
                session.commit()
                session.flush()
                session.close()
            except SQLAlchemyError as e:
                print(e)
                session.rollback()
