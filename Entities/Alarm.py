from sqlalchemy import create_engine, Column, Integer, Boolean, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Alarm(Base):
    def __init__(self, facility_id, sensor_id, elapsed, new_status):
        self.facility_id = facility_id
        self.sensor_id = sensor_id
        self.elapsed = elapsed
        self.new_status = new_status

    def __eq__(self, other):
        return self.sensor_id == other.sensor_id

    def __repr__(self):
        return f"{{'facilityId': {self.facility_id}, 'sensorId': {self.sensor_id}, " \
            f"'elapsed': {self.elapsed}, 'new_status': {self.new_status}}}"

    @property
    def facility_id(self):
        return self.facility_id

    @property
    def sensor_id(self):
        return self.sensor_id

    @sensor_id.setter
    def sensor_id(self, value):
        self._sensor_id = value

    @facility_id.setter
    def facility_id(self, value):
        self._facility_id = value

    __tablename__ = "alarms"

    facility_id = Column('facility_id', Integer)
    sensor_id = Column('sensor_id', Integer, primary_key=True)
    sent = Column('sent', Float)
    received = Column('received', Float)
    elapsed = Column('elapsed', Float)
    new_status = Column('new_status', Boolean)




engine = create_engine('sqlite:///alarms.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

