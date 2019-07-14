def filter_alarm_list(facility_id, sensor_id, alarms):
    no_alarms_facility = f"No alarms found for facility with id {facility_id}"
    no_alarms_sensor = f"No alarms found for sensor with id {sensor_id}"
    no_alarms = f"No alarms found for facility id {facility_id} and sensor id {sensor_id}"

    if not alarms:
        return "No alarms found."

    facility_id = None if facility_id is None else int(facility_id)
    sensor_id = None if sensor_id is None else int(sensor_id)

    if facility_id is None and sensor_id is None:
        return alarms

    elif facility_id is not None and sensor_id is not None:
        alarms = list(filter(lambda a: a.facility_id == facility_id and a.sensor_id == sensor_id, alarms))
        return alarms if alarms else no_alarms

    elif facility_id is not None:
        alarms = list(filter(lambda a: a.facility_id == facility_id, alarms))
        return alarms if alarms else no_alarms_facility

    elif sensor_id is not None:
        alarms = list(filter(lambda a: a.sensor_id == sensor_id, alarms))
        return alarms if alarms else no_alarms_sensor