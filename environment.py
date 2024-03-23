class DayTracker:
    current_day = 1

    @classmethod
    def increment_day(cls):
        cls.current_day += 1

    @classmethod
    def get_current_day(cls):
        return cls.current_day

    @classmethod
    def reset(cls):
        cls.current_day = 1


class Epoch:
    epoch = 1

    @classmethod
    def increment_epoch(cls):
        cls.epoch += 1

    @classmethod
    def get_current_epoch(cls):
        return cls.epoch

    @classmethod
    def reset(cls):
        cls.epoch = 1


class Grid:
    def __init__(self, width, height, resource_points=None):
        self.width = width
        self.height = height
        self.resource_points = resource_points if resource_points else set()
        self.occupied_positions = set()  # Track positions occupied by beings
        self.beings = {}  # Key: Being ID, Value: Being instance

    def add_being(self, being):
        if (being.x, being.y) not in self.occupied_positions:
            self.occupied_positions.add((being.x, being.y))
            self.beings[being.id] = being

    def remove_being(self, being_id):
        being = self.beings.pop(being_id, None)
        if being:
            self.occupied_positions.discard((being.x, being.y))

    def move_being(self, being, dx, dy):
        new_x, new_y = being.x + dx, being.y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.occupied_positions.discard((being.x, being.y))
            being.x, being.y = new_x, new_y
            self.occupied_positions.add((being.x, being.y))

    def simulate_day(self):
        for being in self.beings.values():
            if being.is_active:
                being.update_status()  # Assuming beings have a method to update their status daily
                # Additional daily simulation logic here

    # Additional methods related to the Grid class here (e.g., handling encounters, generating resources)
