# DEPRECATED
class Record:
    def __init__(self, being_id, event_type, description):
        self.epoch = Epoch.get_current_epoch()
        self.day = DayTracker.get_current_day()
        self.being_id = being_id
        self.event_type = event_type
        self.description = description

    def __repr__(self):
        return f"Epoch: {self.epoch}, Day {self.day}, ID:{self.being_id}, {self.event_type}, {self.description}"

#------------------------------------------------------------------


class Log:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
            cls._instance.records = []  # Initialize records only once here
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'records'):  # Ensure that 'records' is only initialized once
            self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_records_by_day(self, day):
        return [record for record in self.records if record.day == day]

    def get_records_by_type(self, event_type):
        return [record for record in self.records if record.event_type == event_type]

    def __repr__(self):
        return "\n".join(str(record) for record in self.records)