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
            epoch=Epoch.get_current_epoch(),
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
            epoch=Epoch.get_current_epoch(),
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
            epoch=Epoch.get_current_epoch(),
            day=DayTracker.get_current_day(),
            x=self.x,
            y=self.y,
            z=self.z,
            encounter_type=encounter_type,
            other_being_id=other_being_id
        )
        self.log.add_encounter_record(encounter_record)


class Human(Entity):
    def __init__(self, x, y, z, grid, resources=random.randint(10, 20), esc_xp=0, win_xp=0, love_xp=0,
                 war_xp=0,
                 theft_chance=0.2):
        super().__init__(x, y, z, grid)
        self.resources = resources
        self.esc_xp = esc_xp
        self.win_xp = win_xp
        self.love_xp = love_xp
        self.war_xp = war_xp
        self.theft_chance = theft_chance
        self.group = None
        self.is_zombie = False

    def become_zombie(self):
        self.lifespan_z = 10
        self.is_zombie = True

    def consume_resources(self):
        self.resources -= 0.5
        self.log.add_resource_record(self.log_resource_change(-0.5, 'DLY'))
        if self.resources <= 0:
            self.become_zombie()

    def move_towards_resource(self):
        if self.resources < 5:
            resource_points = self.grid.get_resource_points_near(self.x, self.y)
            if resource_points:
                target_x, target_y = min(resource_points,
                                         key=lambda point: (point[0] - self.x) ** 2 + (point[1] - self.y) ** 2)
                self.move_towards(target_x, target_y)

    def move_towards_group(self):
        if self.group:
            group_x = sum(member.x for member in self.group.members) / len(self.group.members)
            group_y = sum(member.y for member in self.group.members) / len(self.group.members)
            self.move_towards(group_x, group_y)

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dx = dx // abs(dx) if dx != 0 else 0
        dy = dy // abs(dy) if dy != 0 else 0
        super().move(dx, dy)

    def interact(self, other):
        if isinstance(other, Human):
            self.interact_with_human(other)
        elif isinstance(other, Zombie):
            self.encounter_zombie(other)

    def interact_with_human(self, other_human):
        outcome = random.choices(['love', 'war', 'theft'], weights=[self.love_xp, self.war_xp, self.theft_chance])[0]
        if outcome == 'love':
            self.handle_love_event(other_human)
        elif outcome == 'war':
            self.handle_war_event(other_human)
        elif outcome == 'theft':
            self.handle_theft_event(other_human)

    def handle_love_event(self, other_human):
        love_xp_gain = random.randint(1, (round(other_human.love_xp + 1)))
        self.love_xp += love_xp_gain
        other_human.love_xp += 1

        # Calculate and share resources evenly
        self_prev_res = self.resources
        other_prev_res = other_human.resources
        avg_resources = (self.resources + other_human.resources) / 2
        enc_type = 'LUV'
        self.log_resource_change(change=(avg_resources - self_prev_res), reason=enc_type)
        self.log_resource_change(change=(avg_resources - other_prev_res), reason=enc_type)
        self.log_encounter(encounter_type=enc_type, other_being_id=other_human.id)

        # Handle group logic for love event (group formation or merging)
        self.form_or_merge_group(other_human)

    def handle_war_event(self, other_human):
        if self.war_xp > other_human.war_xp:
            # Current being wins and takes resources from the other being
            war_xp_gain = random.randint(0, (round(other_human.war_xp) + 1))
            self.war_xp += war_xp_gain
            prev_res = other_human.resources
            self.resources += prev_res
            other_human.resources = 0  # The defeated loses all resources
            other_human.is_zombie = True  # becomes a zombie

            # Log the resource change
            enc_type = 'WAR'
            self.log_resource_change(change=prev_res, reason=enc_type)
            self.log_encounter(encounter_type=enc_type, other_being_id=other_human.id)

        elif self.war_xp < other_human.war_xp:
            war_xp_gain = random.randint(0, (round(self.war_xp) + 1))
            other_human.war_xp += war_xp_gain
            prev_res = self.resources
            other_human.resources += self.resources
            self.resources = 0  # The defeated loses all resources
            self.is_zombie = True  # becomes a zombie

            # Log the resource change
            enc_type ='WAR'
            other_human.log_resource_change(change=prev_res, reason=enc_type)
            other_human.log_encounter(encounter_type=enc_type, other_being_id=self.id)

        else:
            self.handle_theft_event(other_human)

    def handle_theft_event(self, other_human):
        if self.theft_chance > other_human.theft_chance:
            # Current being wins and takes resources from the other being
            theft_chance_gain = random.randint(0, (round(other_human.theft_chance) + 1))
            self.theft_chance += theft_chance_gain
            amount = random.randint(0, (other_human.resources + 1))
            self.resources += amount
            other_human.resources -= amount

            # Log the resource change
            self.log_resource_change(change=amount, reason='THF')
            self.log_encounter(encounter_type='THF', other_being_id=other_human.id)

        elif self.theft_chance < other_human.theft_chance:
            theft_chance_gain = random.randint(0, (round(self.theft_chance) + 1))
            other_human.war_xp += theft_chance_gain
            amount = random.randint(0, (self.resources + 1))
            other_human.resources += self.resources
            self.resources -= amount  # The defeated loses all resources

            # Log the resource change
            other_human.log_resource_change(change=amount, reason='THF')
            other_human.log_encounter(encounter_type='THF',other_being_id=self.id)

        else:
            pass

    def form_or_merge_group(self, other_human):
        # If neither is in a group, form a new group
        if not self.group and not other_human.group:
            new_group = Group()
            new_group.add_member(self)
            new_group.add_member(other_human)
        # If one is in a group, add the other
        elif self.group and not other_human.group:
            self.group.add_member(other_human)
        elif not self.group and other_human.group:
            other_human.group.add_member(self)
        # If both are in different groups, consider merging
        elif self.group and other_human.group and self.group != other_human.group:
            self.group.merge_with(other_human.group)

    def encounter_zombie(self, zombie):
        # Determine the outcome of the encounter
        outcome = random.choices(['escape', 'win', 'infected'],
                                 weights=[
                                     self.esc_xp + 1,
                                     self.win_xp + 1,
                                     zombie.infection_chance + 1
                                 ])[0]

        if outcome == 'escape':
            self.esc_xp += 1  # Gain escape experience
            self.log_encounter(encounter_type='ESC', other_being_id=zombie.id)

        elif outcome == 'win':
            win_xp_gain = 1
            self.win_xp += win_xp_gain  # Gain win experience
            self.resources += 2  # Gain resources from the zombie
            zombie.is_active = False  # Zombie is defeated

            self.log_resource_change(change=2,reason='WIN')
            self.log_encounter(encounter_type='WIN', other_being_id=zombie.id)

        elif outcome == 'infected':
            self.become_zombie()  # Human becomes a zombie  # Reset lifespan as a zombie

            self.log_encounter(encounter_type='INF', other_being_id=zombie.id)

    def update_status(self):
        """
        Update the status of a human. If resources run out, they turn into a zombie.
        """
        if self.resources > 0:
            self.resources -= 0.5  # Simulate resource consumption
            # Logging the resource consumption can be done here
        else:
            # Human turns into a zombie if resources run out
            self.is_zombie = True
            self.resources = 0
            # Logging the transition to zombie can be done here

            # If part of a group, remove from the group
            if self.group:
                self.group.remove_member(self)
                self.group = None


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

    def update_status(self):
        """
        Update the status of a zombie. Zombies may decay over time.
        """
          # Simulate the decay of the zombie
        if self.lifespan_z > 1:
            self.lifespan_z -= 1
        else:
            self.lifespan_z = 0
            self.is_active = False # Zombie becomes inactive (decays)
            # Logging decay



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





