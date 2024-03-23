class EncounterLog:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_records_by_day(self, day):
        return [record for record in self.records if record.day == day]


class ResourceLog:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_records_by_day(self, day):
        return [record for record in self.records if record.day == day]


class MovementLog:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_records_by_day(self, day):
        return [record for record in self.records if record.day == day]


class LogRecord:
    def __init__(self, epoch, day, being_id):
        self.epoch = epoch
        self.day = day
        self.being_id = being_id


class EncounterRecord(LogRecord):
    def __init__(self, epoch, day, being_id, encounter_type, x, y, z, other_being_id=None):
        super().__init__(epoch, day, being_id)
        self.encounter_type = encounter_type
        self.x = x
        self.y = y
        self.z = z
        self.other_being_id = other_being_id


class ResourceRecord(LogRecord):
    def __init__(self, epoch, day, being_id, resource_change, current_resources, reason):
        super().__init__(epoch, day, being_id)
        self.resource_change = resource_change
        self.current_resources = current_resources
        self.reason = reason


class MovementRecord(LogRecord):
    def __init__(self, epoch, day, being_id, start_x, start_y, end_x, end_y):
        super().__init__(epoch, day, being_id)
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
