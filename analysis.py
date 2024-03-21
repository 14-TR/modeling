import pandas as pd


def extract_temporal_data(logs):
    # Data structure to hold temporal data
    daily_data = {}

    for record in logs.records:
        day = record.day
        if day not in daily_data:
            daily_data[day] = {'humans': 0, 'zombies': 0, 'human_resources': 0, 'zombie_lifespan': 0}

        if record.event_type == "MOV":  # Assuming movement records contain most of the info
            if not record.is_zombie:
                daily_data[day]['humans'] += 1
                daily_data[day]['human_resources'] += record.resources  # Assuming resources are logged
            else:
                daily_data[day]['zombies'] += 1
                daily_data[day]['zombie_lifespan'] += record.lifespan_z  # Assuming lifespan is logged

    # Calculate averages
    for day, data in daily_data.items():
        if data['humans'] > 0:
            data['avg_human_resources'] = data['human_resources'] / data['humans']
        if data['zombies'] > 0:
            data['avg_zombie_lifespan'] = data['zombie_lifespan'] / data['zombies']

    return daily_data


def extract_encounter_data(logs, encounter_type=None):
    encounter_data = []
    for record in logs.records:
        if encounter_type is None or record.encounter_type == encounter_type:
            encounter_data.append({
                'epoch': record.epoch,
                'day': record.day,
                'being_id': record.being_id,
                'other_being_id': record.other_being_id,
                'encounter_type': record.encounter_type,
                'x': record.x,
                'y': record.y,
                'z': record.z
            })
    return encounter_data


def extract_resource_data(logs):
    # Extracting resource change data from the ResourceLog
    res_data = []
    for record in logs.records:
        res_data = [{
            'Epoch:': record.epoch,
            'Day': record.day,
            'Being ID': record.being_id,
            'Resource Change': record.resource_change,
            'Current Resources': record.current_resources,
            'Reason': record.reason
        } for record in logs.records]

    # Convert the list of dictionaries to a pandas DataFrame
    return pd.DataFrame(res_data)

def extract_movement_data(logs):
    # Extracting movement data from the MovementLog
    mov_data = []
    for record in logs.records:
        mov_data = [{
            'Epoch': record.epoch,
            'Day': record.day,
            'Being ID': record.being_id,
            'Start X': record.start_x,
            'Start Y': record.start_y,
            'End X': record.end_x,
            'End Y': record.end_y
        } for record in logs.records]

    # Convert the list of dictionaries to a pandas DataFrame
    return pd.DataFrame(mov_data)