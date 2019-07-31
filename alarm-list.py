import click
from alarm_filter import filter_alarm_list
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Entities.Alarm import Alarm

Base = declarative_base()
engine = create_engine('sqlite:///alarms.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


@click.command()
@click.option(
    '--facility-id',
    '-f',
    default=None,
    help='List alarms associated with facility with id \'facility_id\'.'
)
@click.option(
    '--sensor-id',
    '-s',
    default=None,
    help='List alarms associated with sensor with id \'sensor_id\'.'
)
def list_alarms(facility_id, sensor_id):
    session = Session()
    try:
        alarms = session.query(Alarm).all()
        filtered = filter_alarm_list(facility_id, sensor_id, alarms)

        if isinstance(filtered, str):
            print(filtered)
        else:
            for alarm in filter_alarm_list(facility_id, sensor_id, alarms):
                print(alarm.__repr__())
            session.commit()
            session.flush()
            session.close()
    except SQLAlchemyError as e:
        print(e)


if __name__ == '__main__':
    list_alarms()
