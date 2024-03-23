import uuid


class LogRecord:
    def __init__(self, being_id, epoch, day, x, y, z):
        self.id = uuid.uuid4()  # Unique identifier for each log record
        self.being_id = being_id
        self.epoch = epoch
        self.day = day
        self.x = x
        self.y = y
        self.z = z


class EncounterRecord(LogRecord):
    def __init__(self, being_id, epoch, day, x, y, z, encounter_type, other_being_id=None):
        super().__init__(being_id, epoch, day, x, y, z)
        self.encounter_type = encounter_type
        self.other_being_id = other_being_id


class ResourceRecord(LogRecord):
    def __init__(self, being_id, epoch, day, x, y, z, resource_change, current_resources, reason):
        super().__init__(being_id, epoch, day, x, y, z)
        self.resource_change = resource_change
        self.current_resources = current_resources
        self.reason = reason


class MovementRecord(LogRecord):
    def __init__(self, being_id, epoch, day, start_x, start_y, end_x, end_y, start_z, end_z):
        super().__init__(being_id, epoch, day, end_x, end_y, end_z)
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        # end_x, end_y, and end_z are already stored in x, y, and z from LogRecord


class Log:
    def __init__(self):
        self.encounter_logs = []
        self.resource_logs = []
        self.movement_logs = []

    def add_encounter_record(self, record):
        self.encounter_logs.append(record)

    def add_resource_record(self, record):
        self.resource_logs.append(record)

    def add_movement_record(self, record):
        self.movement_logs.append(record)

    def get_records_by_day(self, day, log_type='encounter'):
        if log_type == 'encounter':
            return [record for record in self.encounter_logs if record.day == day]
        elif log_type == 'resource':
            return [record for record in self.resource_logs if record.day == day]
        elif log_type == 'movement':
            return [record for record in self.movement_logs if record.day == day]

# Example usage
# log = Log()
# encounter_record = EncounterRecord(being_id='human1', epoch=1, day=1, x=10, y=20, z=5, encounter_type='LUV', other_being_id='human2')
# log.add_encounter_record(encounter_record)
#
# movement_record = MovementRecord(being_id='human1', epoch=1, day=1, start_x=5, start_y=15, start_z=4, end_x=10, end_y=20, end_z=5)
# log.add_movement_record(movement_record)
