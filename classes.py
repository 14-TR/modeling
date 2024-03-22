#########################################################
"""
Title: classes.py
Author: TR Ingram
Description:

This Python script, authored by TR Ingram, orchestrates a simulation where humans and zombies interact within a defined
grid environment. Key components include `DayTracker` and `Epoch` for time tracking, and the `Being` class for
entities with distinct attributes and states, differentiating between humans and zombies.

The `Grid` class sets the stage for these interactions, facilitating movement and encounters that can lead to
transformations (e.g., humans turning into zombies). Events are meticulously logged, providing a detailed narrative
of the simulation's evolution.

Designed to run over a set period, the simulation measures various metrics such as resource distribution and encounter
outcomes, culminating in a dataset that reflects the dynamics of this virtual ecosystem.

"""
#########################################################

import random
from surface_noise import generate_noise


# ==================================================================


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


# ------------------------------------------------------------------


class Epoch:
    epoch = 1

    @classmethod
    def increment_sim(cls):
        cls.epoch += 1

    @classmethod
    def get_current_epoch(cls):
        return cls.epoch

    @classmethod
    def reset(cls):
        cls.epoch = 1


# ------------------------------------------------------------------


class Being:
    last_id = 0

    def __init__(self, x, y, z, resources, is_zombie=False, esc_xp=0, win_xp=0, love_xp=0, war_xp=0, lifespan_z=10,
                 lifespan_h=0):
        Being.last_id += 1
        self.id = Being.last_id
        self.x = x
        self.y = y
        self.z = z
        self.lifespan_h = lifespan_h
        self.resources = resources  # relevant only for humans
        self.is_zombie = is_zombie
        self.esc_xp = esc_xp
        self.win_xp = win_xp
        self.love_xp = love_xp
        self.war_xp = war_xp
        self.lifespan_z = lifespan_z  # Relevant only for zombies
        self.is_active = True
        self.zh_kd = 0  # zombie kills as human
        self.hh_kd = 0  # human kills as human
        self.hz_kd = 0  # human kills as zombie
        self.theft = 0
        self.z_enc = 0
        self.h_enc = 0
        self.path = []

    def move_towards_resource_point(self, resource_points):
        # Find the closest resource point
        closest_point = min(resource_points, key=lambda point: (point[0] - self.x) ** 2 + (point[1] - self.y) ** 2)
        dx = closest_point[0] - self.x
        dy = closest_point[1] - self.y

        # Normalize the movement towards the resource point to ensure it's a single step in the right direction
        dx = dx // abs(dx) if dx != 0 else 0
        dy = dy // abs(dy) if dy != 0 else 0
        return dx, dy

    def move(self, dx, dy, grid, resource_points=set()):
        if not self.is_zombie and resource_points:
            # As resources diminish, increase probability of moving towards resource point
            resource_based_prob = (10 - self.resources) / 10  # Adjust the denominator based on max resources
            if random.random() < resource_based_prob:
                dx, dy = self.move_towards_resource_point(resource_points)
        else:
            new_x = max(0, min(self.x + dx, grid.width - 1))
            new_y = max(0, min(self.y + dy, grid.height - 1))
            current_z = grid.get_elev_at(self.x, self.y)
            new_z = grid.get_elev_at(new_x, new_y)


        # Example: Logging resource replenishment at a resource point
        if (self.x, self.y) in resource_points:
            replenished_amount = min(10 - self.resources, 10)
            self.resources += replenished_amount
            resource_log_instance = ResourceLog()
            resource_log_instance.add_record(
                ResourceRecord(
                    epoch=Epoch.get_current_epoch(),
                    day=DayTracker.get_current_day(),
                    being_id=self.id,
                    resource_change=replenished_amount,
                    current_resources=self.resources,
                    reason="resource_point_replenishment"
                )
            )

        # Check if the being is a zombie and if it's moving uphill
        if self.is_zombie:
            new_x = max(0, min(round(self.x + dx), grid.width - 1))
            new_y = max(0, min(round(self.y + dy), grid.height - 1))
            current_z = grid.get_elev_at(self.x, self.y)
            new_z = grid.get_elev_at(new_x, new_y)

            if new_z > current_z:
                # Adjust dx and dy for uphill movement
                dx /= 2
                dy /= 2

            # Round dx and dy to ensure they are integers
        dx = round(dx)
        dy = round(dy)

        # Calculate new position with rounded deltas
        new_x = max(0, min(self.x + dx, grid.width - 1))
        new_y = max(0, min(self.y + dy, grid.height - 1))
        new_z = grid.get_elev_at(new_x, new_y)

        if not self.is_zombie:
            # Human: Increase resource consumption if moving uphill
            if new_z > self.z:
                self.resources -= ((new_z - self.z) + .5)  # Adjust this formula as needed

                # Log the resource change
                resource_log_instance = ResourceLog()
                resource_log_instance.add_record(
                    ResourceRecord(
                        epoch=Epoch.get_current_epoch(),
                        day=DayTracker.get_current_day(),
                        being_id=self.id,
                        resource_change=((new_z - self.z) + .5) ,  # Amount of resources changed
                        current_resources=self.resources,  # Current resources after the change
                        reason="movement"  # Reason for the resource change
                    )
                )

            # Standard movement cost for humans
            self.resources -= 0.5

            # Log the resource change
            resource_log_instance = ResourceLog()
            resource_log_instance.add_record(
                ResourceRecord(
                    epoch=Epoch.get_current_epoch(),
                    day=DayTracker.get_current_day(),
                    being_id=self.id,
                    resource_change=-0.5,  # Amount of resources changed
                    current_resources=self.resources,  # Current resources after the change
                    reason="movement"  # Reason for the resource change
                )
            )

        else:
            # Zombie: Decrease lifespan with each move
            self.lifespan_z -= 1

        # Update being's position if it has enough resources/lifespan
        if (not self.is_zombie and self.resources > 0) or (self.is_zombie and self.lifespan_z > 0):
            self.x = new_x
            self.y = new_y
            self.z = new_z

            move_log_instance = MovementLog()

            move_log_instance.add_record(
                MovementRecord(
                    epoch=Epoch.get_current_epoch(),
                    day=DayTracker.get_current_day(),
                    being_id=self.id,
                    start_x=self.x,  # Assuming you store the starting position
                    start_y=self.y,  # Assuming you store the starting position
                    end_x=self.x,  # The new x position after movement
                    end_y=self.y  # The new y position after movement
                )
            )

        # placeholder logic if the being can't move (e.g., not enough resources)

    def encounter(self, other):
        if self.is_zombie:
            self.encounter_as_zombie(other)
        else:
            if other.is_zombie:
                self.encounter_zombie(other)
            else:
                self.encounter_human(other)

    def encounter_as_zombie(self, other):
        if not other.is_zombie:  # If the other being is not a zombie
            # The chance of getting infected is based on the human's ability to escape or win, see weights below
            is_infected = random.choices(
                [True, False],  # True for infected, False for not infected
                weights=[.5, other.esc_xp + other.win_xp]
                # Weights: infection vs. escape or win, this similar structure is used throughout
            )

            if is_infected:
                # Human gets infected and becomes a zombie
                other.is_zombie = True
                self.lifespan_z += 3  # The infecting zombie's lifespan increases
                self.hz_kd += 1  # Increment the count of humans killed as a zombie-MAY NEED CORRECTION?

                enc_log_instance = EncounterLog()

                enc_log_instance.add_record(
                    EncounterRecord(epoch=Epoch.get_current_epoch(),
                                    day=DayTracker.get_current_day(),
                                    being_id=self.id,
                                    other_being_id=other.id,
                                    encounter_type="INF",
                                    x=self.x,
                                    y=self.y,
                                    z=self.z)
                )

    def encounter_zombie(self, zombie):
        # Escape, Win (kill), or be turned into zombie.
        outcome = random.choices(['escape', 'win', 'infected'], weights=[self.esc_xp + 1, self.win_xp + 1, 2])[0]

        if outcome == 'escape':
            self.esc_xp += 1  # Gain escape experience
            self.z_enc += 1
            enc_log_instance = EncounterLog()
            enc_log_instance.add_record(
                EncounterRecord(epoch=Epoch.get_current_epoch(),
                                day=DayTracker.get_current_day(),
                                being_id=self.id,
                                other_being_id=zombie.id,
                                encounter_type="ESC",
                                x=self.x,
                                y=self.y,
                                z=self.z)
            )
        elif outcome == 'win':
            self.win_xp += random.randint(0, (zombie.win_xp + 1))  # Gain win experience
            self.resources += zombie.resources  # Gain a small amount of resources
            # Log the resource change
            resource_log_instance = ResourceLog()
            resource_log_instance.add_record(
                ResourceRecord(
                    epoch=Epoch.get_current_epoch(),
                    day=DayTracker.get_current_day(),
                    being_id=self.id,
                    resource_change=+zombie.resources,  # Amount of resources changed
                    current_resources=self.resources,  # Current resources after the change
                    reason="movement"  # Reason for the resource change
                )
            )
            # kill the zombie
            zombie.is_active = False
            self.zh_kd += 1
            enc_log_instance = EncounterLog()
            enc_log_instance.add_record(
                EncounterRecord(epoch=Epoch.get_current_epoch(),
                                day=DayTracker.get_current_day(),
                                being_id=self.id,
                                other_being_id=zombie.id,
                                encounter_type="WIN",
                                x=self.x,
                                y=self.y,
                                z=self.z)
            )
        else:  # infected
            self.is_zombie = True
            self.lifespan_z = 10  # Reset lifespan zombie
            enc_log_instance = EncounterLog()
            enc_log_instance.add_record(
                EncounterRecord(epoch=Epoch.get_current_epoch(),
                                day=DayTracker.get_current_day(),
                                being_id=zombie.id,
                                other_being_id=zombie.id,
                                encounter_type="INF",
                                x=self.x,
                                y=self.y,
                                z=self.z)
            )

        self.z_enc += 1

    def encounter_human(self, other_human):
        # Decide the outcome: love or war, ensuring weights are never zero by adding a small value
        outcome = random.choices(['love', 'war'], weights=[self.love_xp + 0.1, self.war_xp + 0.1])[0]
        # self_id = f"{self.id}"
        # other_human_id = f"{other_human.id}"
        if outcome == 'love':
            self.love_xp += random.randint(0, (other_human.love_xp + 1))  # Gain love experience
            other_human.love_xp += 1
            avg_resources = (self.resources + other_human.resources) / 2
            self.resources = other_human.resources = avg_resources  # Even out resources############
            resource_log_instance = ResourceLog()
            resource_log_instance.add_record(
                ResourceRecord(
                    epoch=Epoch.get_current_epoch(),
                    day=DayTracker.get_current_day(),
                    being_id=self.id,
                    resource_change=+self.resources - avg_resources,  # Amount of resources changed
                    current_resources=self.resources,  # Current resources after the change
                    reason="movement"  # Reason for the resource change
                )
            )
            self.h_enc += 1
            enc_log_instance = EncounterLog()
            enc_log_instance.add_record(
                EncounterRecord(epoch=Epoch.get_current_epoch(),
                                day=DayTracker.get_current_day(),
                                being_id=self.id,
                                other_being_id=other_human.id,
                                encounter_type="LUV",
                                x=self.x,
                                y=self.y,
                                z=self.z)
            )

        else:
            if self.war_xp > other_human.war_xp:
                self.war_xp += random.randint(0, (other_human.war_xp + 1))  # Gain war experience
                self.resources += other_human.resources  # Take all resources from the defeated
                resource_log_instance = ResourceLog()
                resource_log_instance.add_record(
                    ResourceRecord(
                        epoch=Epoch.get_current_epoch(),
                        day=DayTracker.get_current_day(),
                        being_id=self.id,
                        resource_change=+other_human.resources,  # Amount of resources changed
                        current_resources=self.resources,  # Current resources after the change
                        reason="WAR"  # Reason for the resource change
                    )
                )
                other_human.resources = 0  # The defeated loses all resources
                other_human.is_zombie = True  # The defeated becomes a zombie
                self.hh_kd += 1
                self.h_enc += 1
                enc_log_instance = EncounterLog()
                enc_log_instance.add_record(
                    EncounterRecord(epoch=Epoch.get_current_epoch(),
                                    day=DayTracker.get_current_day(),
                                    being_id=self.id,
                                    other_being_id=other_human.id,
                                    encounter_type="WAR",
                                    x=self.x,
                                    y=self.y,
                                    z=self.z)
                )
            else:
                if self.war_xp == other_human.war_xp:
                    theft_outcome = random.choices(['theft', 'war'], weights=[self.theft + 0.1, self.war_xp + 0.1])[0]
                    if theft_outcome == 'theft':
                        self.theft += 1
                        amount = random.randint(0, round(other_human.resources + 1))
                        self.resources += amount
                        resource_log_instance = ResourceLog()
                        resource_log_instance.add_record(
                            ResourceRecord(
                                epoch=Epoch.get_current_epoch(),
                                day=DayTracker.get_current_day(),
                                being_id=self.id,
                                resource_change=+amount,  # Amount of resources changed
                                current_resources=self.resources,  # Current resources after the change
                                reason="movement"  # Reason for the resource change
                            )
                        )
                        other_human.resources -= amount
                        resource_log_instance = ResourceLog()
                        resource_log_instance.add_record(
                            ResourceRecord(
                                epoch=Epoch.get_current_epoch(),
                                day=DayTracker.get_current_day(),
                                being_id=other_human.id,
                                resource_change=-amount,  # Amount of resources changed
                                current_resources=other_human.resources,  # Current resources after the change
                                reason="movement"  # Reason for the resource change
                            )
                        )
                        enc_log_instance = EncounterLog()
                        enc_log_instance.add_record(
                            EncounterRecord(epoch=Epoch.get_current_epoch(),
                                            day=DayTracker.get_current_day(),
                                            being_id=self.id,
                                            other_being_id=other_human.id,
                                            encounter_type="STL",
                                            x=self.x,
                                            y=self.y,
                                            z=self.z)
                        )
                        if other_human.theft > 1:
                            other_human.theft -= 1
                            enc_log_instance = EncounterLog()
                            enc_log_instance.add_record(
                                EncounterRecord(epoch=Epoch.get_current_epoch(),
                                                day=DayTracker.get_current_day(),
                                                being_id=self.id,
                                                other_being_id=other_human.id,
                                                encounter_type="ROB",
                                                x=self.x,
                                                y=self.y,
                                                z=self.z)
                            )
                        else:
                            other_human.theft = 0
                            other_human.is_zombie = True

                    else:
                        self.war_xp += random.randint(0, (other_human.war_xp + 1))  # Gain war experience
                        self.resources += other_human.resources  # Take all resources from the defeated
                        resource_log_instance = ResourceLog()
                        resource_log_instance.add_record(
                            ResourceRecord(
                                epoch=Epoch.get_current_epoch(),
                                day=DayTracker.get_current_day(),
                                being_id=self.id,
                                resource_change=+other_human.resources,  # Amount of resources changed
                                current_resources=self.resources,  # Current resources after the change
                                reason="movement"  # Reason for the resource change
                            )
                        )
                        other_human.resources = 0  # The defeated loses all resources
                        other_human.is_zombie = True  # The defeated becomes a zombie
                        self.hh_kd += 1
                        self.h_enc += 1
                        enc_log_instance = EncounterLog()
                        enc_log_instance.add_record(
                            EncounterRecord(epoch=Epoch.get_current_epoch(),
                                            day=DayTracker.get_current_day(),
                                            being_id=self.id,
                                            other_being_id=other_human.id,
                                            encounter_type="WAR",
                                            x=self.x,
                                            y=self.y,
                                            z=self.z)
                        )

    def update_status(self):
        if self.is_zombie:
            self.lifespan_z -= 1  # Simulate the decay of the zombie
            if self.lifespan_z <= 0:
                self.is_active = False
                # print(f"Being {self.id} (zombie) decayed.")
        else:
            if self.resources > 0:
                self.resources -= 0.5  # Simulate resource consumption for humans
                self.lifespan_h += 1
            else:
                self.is_zombie = True
                self.resources = 0  # Human becomes a zombie
                # print(f"Being {self.id} (human) starved.")


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

class Grid:
    def __init__(self, width, height,resource_points=None):
        self.width = width
        self.height = height
        self.beings = []
        self.rmv_beings = 0
        self.occupied_positions = set()
        self.surface = None
        self.resource_points = resource_points if resource_points else set()

    def generate_resource_points(self, num_points):
        points = set()
        while len(points) < num_points:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            points.add((x, y))
        return points

    def add_being(self, being):
        while (being.x, being.y) in self.occupied_positions:  # Check if position is occupied
            # Generate new positions until an unoccupied one is found
            being.x = random.randint(0, self.width - 1)
            being.y = random.randint(0, self.height - 1)
        self.occupied_positions.add((being.x, being.y))  # Mark the new position as occupied
        self.beings.append(being)

    def move_being(self, being):
        h_move = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        z_move = [-2, -1, 0, 1, 2]
        if not being.is_zombie:
            dx = random.choice(z_move)
            dy = random.choice(z_move)
        else:
            dx = random.choice(h_move)
            dy = random.choice(h_move)

        # Store the current position
        current_x, current_y = being.x, being.y

        # Being attempts to move (the move method will handle resource/lifespan checks)
        being.move(dx, dy, self, self.resource_points)

        # If the move was successful (the being's position changed), update occupied positions
        if (current_x, current_y) != (being.x, being.y):
            # Remove the old position if it exists in the set
            if (current_x, current_y) in self.occupied_positions:
                self.occupied_positions.remove((current_x, current_y))

            # Add the new position
            self.occupied_positions.add((being.x, being.y))

    def simulate_day(self):
        for being in list(self.beings):  # using a list copy here to avoid issues while modifying the list
            if being.is_active:
                self.move_being(being)
                for other in list(self.beings):
                    if being.is_active and other.is_active and being != other:
                        if abs(being.x - other.x) <= 1 and abs(being.y - other.y) <= 1:
                            being.encounter(other)
                being.update_status()

        # Now remove inactive beings
        self.remove_inactive_beings()

    def remove_inactive_beings(self):
        self.beings = [being for being in self.beings if being.is_active]
        # add to the number of beings removed the number self.beings list gains
        self.occupied_positions = {(being.x, being.y) for being in self.beings}

    def count_humans_and_zombies(self):
        humans = sum(1 for being in self.beings if not being.is_zombie and being.is_active)
        zombies = sum(1 for being in self.beings if being.is_zombie and being.is_active)
        return humans, zombies

    # append the surface generated in surface_noise.py to the grid
    def append_surface(self, surface):
        self.surface = surface

    def get_elev_at(self, x, y):
        if self.surface is None:
            return 0
        else:
            return self.surface[x, y]


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


# class Record:
#     def __init__(self, epoch, day, being_id, event_type, description, x, y, z):
#         self.epoch = epoch
#         self.day = day
#         self.being_id = being_id
#         self.event_type = event_type
#         self.description = description
#         self.x = x
#         self.y = y
#         self.z = z
#
#     def __repr__(self):
#         return (f"Epoch: {self.epoch}, "
#                 f"Day {self.day}, "
#                 f"ID:{self.being_id}, "
#                 f"Type: {self.event_type}, "
#                 f"Desc: {self.description},"
#                 f"Z: {self.z}")

# ------------------------------------------------------------------


class EncounterRecord:
    def __init__(self, epoch, day, being_id, other_being_id, encounter_type, x, y, z):
        self.epoch = epoch
        self.day = day
        self.being_id = being_id
        self.other_being_id = other_being_id
        self.encounter_type = encounter_type
        self.x = x,
        self.y = y,
        self.z = z


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


class EncounterLog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EncounterLog, cls).__new__(cls)
            cls._instance.records = []  # Initialize records only once
        return cls._instance

    def add_record(self, record):
        self.records.append(record)

    def get_records_by_day(self, day):
        return [record for record in self.records if record.day == day]


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


class ResourceRecord:
    def __init__(self, epoch, day, being_id, resource_change, current_resources, reason):
        self.epoch = epoch
        self.day = day
        self.being_id = being_id
        self.resource_change = resource_change
        self.current_resources = current_resources
        self.reason = reason  # e.g., "consumption", "encounter_win"


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
class ResourceLog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceLog, cls).__new__(cls)
            cls._instance.records = []  # Initialize records only once
        return cls._instance

    def add_record(self, record):
        self.records.append(record)

    def get_records_by_day(self, day):
        return [record for record in self.records if record.day == day]


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


class MovementRecord:
    def __init__(self, epoch, day, being_id, start_x, start_y, end_x, end_y):
        self.epoch = epoch
        self.day = day
        self.being_id = being_id
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    #get is zombie status
    def get_is_zombie(self, being_id):
        for being in self.beings:
            if being.id == being_id:
                return being.is_zombie
        return False




# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


class MovementLog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MovementLog, cls).__new__(cls)
            cls._instance.records = []  # Initialize records only once
        return cls._instance

    def add_record(self, record):
        self.records.append(record)

    def get_records_by_day(self, day):
        return [record for record in self.records if record.day == day]

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# class Log:
#     _instance = None
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(Log, cls).__new__(cls)
#             cls._instance.records = []  # Initialize records only once
#         return cls._instance
#
#     def __init__(self):
#         if not hasattr(self, 'records'):  # Ensures 'records' is only initialized once
#             self.records = []
#
#     def add_record(self, record):
#         self.records.append(record)
#
#     def get_records_by_day(self, day):
#         return [record for record in self.records if record.day == day]
#
#     def get_records_by_type(self, event_type):
#         return [record for record in self.records if record.event_type == event_type]
#
#     def __repr__(self):
#         return "\n".join(str(record) for record in self.records)
