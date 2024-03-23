import random

import numpy as np


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
    def __init__(self, width, height, elevation_data=None, resource_points=None):
        self.width = width
        self.height = height
        self.active_entities = {}  # Dictionary to store active entities by their ID
        self.final_entities = {}  # Dictionary to store inactive (final) entities by their ID
        self.elevation_data = elevation_data if elevation_data is not None else self.generate_default_elevation()
        self.resource_points = resource_points if resource_points else set()

    def add_entity(self, entity):
        """Add an entity to the grid."""
        self.active_entities[entity.id] = entity

    def deactivate_entity(self, entity_id):
        """Move an entity from active to final (inactive) entities."""
        if entity_id in self.active_entities:
            entity = self.active_entities.pop(entity_id)  # Remove from active and get the entity
            self.final_entities[entity_id] = entity  # Add to final

    def simulate_day(self):
        already_interacted = set()

        for entity_id, entity in list(self.active_entities.items()):
            # Randomly decide the entity's movement direction
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            # Call the entity's move method with the determined dx and dy
            entity.move(dx, dy)

            # Check for interactions with other entities
            for other_id, other in list(self.active_entities.items()):
                if other_id != entity_id:
                    pair = frozenset([entity_id, other_id])
                    if pair not in already_interacted:
                        entity.interact(other)  # Ensure entities have an interact method
                        already_interacted.add(pair)

            # Update the entity's status after potential interactions
            entity.update_status()

            # If the entity is no longer active after updating its status, move it to final entities
            if not entity.is_active:
                self.deactivate_entity(entity_id)

    def generate_default_elevation(self):
        """Generate default flat elevation data for the grid."""
        return np.zeros((self.height, self.width))

    def get_elevation_at(self, x, y):
        """Get the elevation at the specified coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.elevation_data[y][x]
        return 0  # Return a default value if out of bounds

