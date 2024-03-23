class Event:
    def __init__(self, event_type, data):
        self.event_type = event_type
        self.data = data  # Data can contain any relevant information for the event

class EventQueue:
    def __init__(self):
        self.queue = []

    def add_event(self, event):
        self.queue.append(event)

    def get_next_event(self):
        return self.queue.pop(0) if self.queue else None

class EventHandler:
    def handle_event(self, event):
        # Process the event
        # This method can be extended or overridden in subclasses for specific event types
        pass
