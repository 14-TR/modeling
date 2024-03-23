import random

import numpy as np

from environment import Epoch, DayTracker
from logs import MovementRecord, ResourceRecord, EncounterRecord


# Base Entity class for all entities in the simulation
class Entity:
    last_id = 0

    def __init__(self, x, y, z, grid):
        Entity.last_id += 1
        self.id = Entity.last_id
        self.x = x
        self.y = y
        self.z = z
        self.grid = grid
        self.is_active = True
        self.lifespan_z = 10
        self.log = None

    def set_log_instance(self, log_instance):
        self.log = log_instance

    def move(self, dx, dy):
        start_x, start_y, start_z = self.x, self.y, self.grid.get_elevation_at(self.x, self.y)
        self.x = max(0, min(self.x + dx, self.grid.width - 1))
        self.y = max(0, min(self.y + dy, self.grid.height - 1))
        end_x, end_y, end_z = self.x, self.y, self.grid.get_elevation_at(self.x, self.y)
        # Log the movement
        self.log_movement(start_x, start_y, start_z)

    def log_movement(self, start_x, start_y, start_z):
        movement_record = MovementRecord(
            being_id=self.id,
            epoch=Epoch.get_current_epoch,
            day=DayTracker.get_current_day(),
            start_x=start_x,
            start_y=start_y,
            start_z=start_z,
            end_x=self.x,
            end_y=self.y,
            end_z=self.z
        )
        self.log.add_movement_record(movement_record)

    def log_resource_change(self, change, reason):
        resource_record = ResourceRecord(
            being_id=self.id,
            epoch=Epoch.get_current_epoch,
            day=DayTracker.get_current_day(),
            x=self.x,
            y=self.y,
            z=self.z,
            resource_change=change,
            current_resources=self.resources,  # Assuming entities have resources
            reason=reason
        )
        self.log.add_resource_record(resource_record)

    def log_encounter(self, other_being_id, encounter_type):
        encounter_record = EncounterRecord(
            being_id=self.id,
            epoch=Epoch.get_current_epoch,
            day=DayTracker.get_current_day(),
            x=self.x,
            y=self.y,
            z=self.z,
            encounter_type=encounter_type,
            other_being_id=other_being_id
        )
        self.log.add_encounter_record(encounter_record)


class Human(Entity):
    def __init__(self, x, y, z, grid, resources=None, esc_xp=0, win_xp=0, love_xp=0, war_xp=0, theft_chance=0.2):
        super().__init__(x, y, z, grid)
        self.resources = resources if resources is not None else random.randint(10, 20)
        self.esc_xp = esc_xp
        self.win_xp = win_xp
        self.love_xp = love_xp
        self.war_xp = war_xp
        self.theft_chance = theft_chance
        self.group = None
        self.is_zombie = False

    # Other methods remain the same...


# Zombie class, also inheriting from Entity
class Horde:
    last_horde_id = 0

    def __init__(self):
        Horde.last_horde_id += 1
        self.id = Horde.last_horde_id
        self.members = []  # List to store member Zombies

    def add_member(self, zombie):
        """Add a Zombie to the horde."""
        if zombie not in self.members:
            self.members.append(zombie)
            zombie.horde = self  # Link the zombie back to this horde

    def remove_member(self, zombie):
        """Remove a Zombie from the horde."""
        if zombie in self.members:
            self.members.remove(zombie)
            zombie.horde = None  # Unlink the zombie from this horde

    def move_together(self):
        """Move all members of the horde together towards a target or randomly."""
        # Example: Move towards the nearest human or just wander around
        for zombie in self.members:
            if zombie.is_active:
                # Here you can implement logic for horde movement
                # For example, moving towards the nearest human or group of humans
                dx, dy = zombie.decide_movement()  # This method should be defined in the Zombie class
                zombie.move(dx, dy)

    def infect_together(self, target):
        """Attempt to infect a target together, increasing the chances of infection."""
        for zombie in self.members:
            if zombie.is_active:
                zombie.infect(target)


# Update the Zombie class to include horde behavior
class Zombie(Entity):
    def __init__(self, x, y, z, grid, infection_chance=0.3):
        super().__init__(x, y, z, grid)
        self.infection_chance = infection_chance
        self.horde = None  # Initially, the zombie is not part of any horde

    # Define methods for zombie behavior, including infecting humans and possibly horde behavior...

    def join_horde(self, horde):
        """Join the zombie to a horde."""
        if self.horde is not None:
            self.horde.remove_member(self)
        horde.add_member(self)

    def leave_horde(self):
        """Leave the current horde."""
        if self.horde is not None:
            self.horde.remove_member(self)
            self.horde = None

    def decide_movement(self):
        """Decide the next movement for the zombie, possibly influenced by horde behavior or other factors."""
        if self.horde and self.horde.members:
            # Move towards the average position of the horde
            avg_x = sum(zombie.x for zombie in self.horde.members) / len(self.horde.members)
            avg_y = sum(zombie.y for zombie in self.horde.members) / len(self.horde.members)
            dx = (avg_x - self.x) / max(abs(avg_x - self.x), 1)  # Normalize to -1, 0, or 1
            dy = (avg_y - self.y) / max(abs(avg_y - self.y), 1)  # Normalize to -1, 0, or 1
        else:
            # Check for nearby humans
            closest_human, min_distance = self.find_closest_human()
            if closest_human and min_distance < 10:  # Assuming zombies are attracted to humans within a distance of 10 units
                # Move towards the closest human
                dx = (closest_human.x - self.x) / max(abs(closest_human.x - self.x), 1)  # Normalize to -1, 0, or 1
                dy = (closest_human.y - self.y) / max(abs(closest_human.y - self.y), 1)  # Normalize to -1, 0, or 1
            else:
                # Random wandering
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])

        return int(dx), int(dy)

    def find_closest_human(self):
        """Find the closest human to this zombie."""
        closest_human = None
        min_distance = float('inf')
        for entity in self.grid.entities:
            if isinstance(entity, Human) and entity.is_active:
                distance = self.calculate_distance(entity.x, entity.y)
                if distance < min_distance:
                    closest_human = entity
                    min_distance = distance
        return closest_human, min_distance

    def calculate_distance(self, x, y):
        """Calculate the distance from this zombie to a point (x, y)."""
        return ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5

    def infect(self, target):
        """Attempt to infect a target, potentially turning them into a zombie."""
        if random.random() < self.infection_chance:
            # Infection logic here
            target.become_zombie()


# Group class for managing groups of humans
class Group:
    last_group_id = 0

    def __init__(self):
        Group.last_group_id += 1
        self.id = Group.last_group_id
        self.members = []

    def add_member(self, being):
        self.members.append(being)
        being.group = self

    def remove_member(self, being):
        self.members.remove(being)
        being.group = None

    def share_resources_among_adjacent_members(self):
        for member in self.members:
            adjacent_members = self.find_adjacent_members(member)
            if adjacent_members:
                total_resources = sum(m.resources for m in adjacent_members) + member.resources
                avg_resources = total_resources / (len(adjacent_members) + 1)
                for m in adjacent_members:
                    m.resources = avg_resources
                member.resources = avg_resources

    def assist_in_encounters(self, member, other):
        adjacent_members = self.find_adjacent_members(member)
        for adj_member in adjacent_members:
            if isinstance(other, Zombie):
                adj_member.assist_in_zombie_encounter(member, other)
            elif isinstance(other, Human):
                adj_member.assist_in_human_encounter(member, other)

    def find_adjacent_members(self, member):
        adjacent_members = []
        for m in self.members:
            if m is not member and abs(m.x - member.x) <= 1 and abs(m.y - member.y) <= 1:
                adjacent_members.append(m)
        return adjacent_members





