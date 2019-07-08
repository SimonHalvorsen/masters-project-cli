import click
from kafka_alarm_consumer import alarms
from alarm_filter import filter_alarm_list


@click.command()
@click.option(
    '--facility_id',
    '-f',
    help='List alarms associated with facility with \'facility_id\'. Default lists alarms from all facilities.'
)
@click.option(
    '--sensor_id',
    '-s',
    help='List alarms associated with sensor with \'sensor_id\'. Default lists alarms from all sensors.'
)
def list_alarms(facility_id=None, sensor_id=None):
    print(alarms)
    print(filter_alarm_list(facility_id, sensor_id, alarms))


if __name__ == '__main__':
    list_alarms()
