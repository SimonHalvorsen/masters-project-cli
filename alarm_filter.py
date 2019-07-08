def filter_alarm_list(facility_id, sensor_id, alarms):
    no_alarms_facility = "No alarms found for facility with id {}".format(facility_id)
    no_alarms_sensor = "No alarms found for sensor with id {}".format(sensor_id)

    if not alarms:
        return "No alarms found."

    facility_id = int(facility_id) if not None else None
    sensor_id = int(sensor_id) if not None else None

    if facility_id is not None and sensor_id is not None:
        return alarms

    elif facility_id is not None:
        alarms = filter(lambda a: a['facilityId'] == facility_id, alarms)
        return alarms if alarms else no_alarms_facility
    elif sensor_id is not None:
        alarms = filter(lambda a: a['sensorId'] == sensor_id, alarms)
        return alarms if alarms else no_alarms_sensor