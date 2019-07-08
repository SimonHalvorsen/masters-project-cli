from kafka import KafkaConsumer
from json import loads
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from Entities.Alarm import Alarm
from datetime import datetime

bootstrap_server, topic = map(str.strip, open('bootstrapservers.txt', 'r').read().split(','))

Base = declarative_base()
engine = create_engine('sqlite:///alarms.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


consumer = KafkaConsumer(
    topic,
    bootstrap_servers=[bootstrap_server],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='cli',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)


while True:
    session = Session()

    data = consumer.poll(timeout_ms=100)

    for _, messages in data.items():
        for message in messages:
            print(message.value)
            try:
                value = message.value
                sent = datetime.fromtimestamp(value['timestamp'])
                received = datetime.now()
                elapsed = (received - sent).total_seconds()

                alarm = Alarm(value['facilityId'], value['sensorId'], elapsed, 1)
                print(alarm)

            except ValueError as e:
                print(e)
            try:
                session.merge(alarm)
                alarms = session.query(Alarm).all()
                for alarm in alarms:
                    print(alarm.__repr__() + " persisted.")
                session.commit()
                session.flush()
            except SQLAlchemyError as e:
                print(e)
                print("IEFUGHDIVFBEWFIJVFRHEIJSDNJ VFJØLDFHJNGFKLVDSFJGNBESRFDILSJNJKDS")
                session.rollback()
