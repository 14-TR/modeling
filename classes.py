import random

#==================================================================
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


#------------------------------------------------------------------


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




#------------------------------------------------------------------


class Being:
    last_id = 0

    def __init__(self, x, y, resources, is_zombie=False, esc_xp=0, win_xp=0, love_xp=0, war_xp=0, lifespan_z=10, lifespan_h=0):
        Being.last_id += 1
        self.id = Being.last_id
        self.x = x
        self.y = y
        self.lifespan_h = lifespan_h
        self.resources = resources # relevant only for humans
        self.is_zombie = is_zombie
        self.esc_xp = esc_xp
        self.win_xp = win_xp
        self.love_xp = love_xp
        self.war_xp = war_xp
        self.lifespan_z = lifespan_z  # Relevant only for zombies
        self.is_active = True
        self.zh_kd = 0 #zombie kills as human
        self.hh_kd = 0 #human kills as human
        self.hz_kd = 0 #human kills as zombie
        self.theft = 0
        self.z_enc = 0
        self.h_enc = 0
        self.path = []

    def move(self, dx, dy, grid):
        # Ensure the being stays within the grid
        self.x = max(0, min(self.x + dx, grid.width - 1))
        self.y = max(0, min(self.y + dy, grid.height - 1))
        log_instance = Log()
        details = f"moved to ({dx}, {dy})"
        # Example of logging a movement event
        log_instance.add_record(Record(epoch=Epoch.get_current_epoch(),
                                       day=DayTracker.get_current_day(),
                                       being_id=f"{self.id}",
                                       event_type="MOV",
                                       description=details))

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
            # The chance of getting infected is based on the human's ability to escape or win
            is_infected = random.choices(
                [True, False],  # True for infected, False for not infected
                weights=[2, other.esc_xp + other.win_xp]  # Weights: infection vs. escape or win
            )[0]  # [0] to get the first item from the list

            if is_infected:
                # Human gets infected and becomes a zombie
                other.is_zombie = True
                self.lifespan_z += 3  # The infecting zombie's lifespan increases
                self.hz_kd += 1  # Increment the count of humans killed as a zombie- take a look at this for correct logic
                log_instance = Log()
                details = f"contacted {other.id} @ {self.x, self.y}"
                log_instance.add_record(
                    Record(epoch=Epoch.get_current_epoch(),
                           day=DayTracker.get_current_day(),
                           being_id=f"{self.id}",
                           event_type="INF",
                           description=details))

    def encounter_zombie(self, zombie):
        # Decide the outcome: escape, win, or get infected
        outcome = random.choices(['escape', 'win', 'infected'], weights=[self.esc_xp + 1, self.win_xp + 1, 2])[0]
        self_id = f"{self.id}"
        if outcome == 'escape':
            self.esc_xp += 1  # Gain escape experience
            self.z_enc += 1
            log_instance = Log()
            details = f"contacted {zombie.id} @ {self.x, self.y}"
            log_instance.add_record(
                Record(epoch=Epoch.get_current_epoch(),
                       day=DayTracker.get_current_day(),
                       being_id=f"{self.id}",
                       event_type="ESC",
                       description=details))
        elif outcome == 'win':
            self.win_xp += 1  # Gain win experience
            self.resources += zombie.resources  # Gain a small amount of resources
            # kill the zombie
            zombie.is_active = False
            self.zh_kd += 1
            log_instance = Log()
            details = f"contacted {zombie.id} @ {self.x, self.y}"
            log_instance.add_record(
                Record(epoch=Epoch.get_current_epoch(),
                       day=DayTracker.get_current_day(),
                       being_id=f"{self.id}",
                       event_type="WIN",
                       description=details))
        else:  # infected
            self.is_zombie = True
            self.lifespan_z = 10  # Reset lifespan as a zombie
            log_instance = Log()
            details = f"contacted Z-{zombie.id} @ {self.x, self.y}"
            log_instance.add_record(
                Record(epoch=Epoch.get_current_epoch(),
                       day=DayTracker.get_current_day(),
                       being_id=f"{self.id}",
                       event_type="INF",
                       description=details))

        self.z_enc += 1

    def encounter_human(self, other_human):
        # Decide the outcome: love or war, ensuring weights are never zero by adding a small value
        outcome = random.choices(['love', 'war'], weights=[self.love_xp + 0.1, self.war_xp + 0.1])[0]
        self_id = f"{self.id}"
        other_human_id = f"{other_human.id}"
        if outcome == 'love':
            self.love_xp += 1  # Gain love experience
            other_human.love_xp += 1
            avg_resources = (self.resources + other_human.resources) / 2
            self.resources = other_human.resources = avg_resources  # Even out resources
            self.h_enc += 1
            log_instance = Log()
            details = f"contacted {other_human.id} @ {self.x, self.y}"
            log_instance.add_record(
                Record(epoch=Epoch.get_current_epoch(),
                       day=DayTracker.get_current_day(),
                       being_id=f"{self.id}",
                       event_type="LUV",
                       description=details))

        else:
            if self.war_xp > other_human.war_xp:
                self.war_xp += 1  # Gain war experience
                self.resources += other_human.resources  # Take all resources from the defeated
                other_human.resources = 0  # The defeated loses all resources
                other_human.is_zombie = True  # The defeated becomes a zombie
                self.hh_kd += 1
                self.h_enc += 1
                log_instance = Log()
                details = f"contacted {other_human.id} @ {self.x, self.y}"
                log_instance.add_record(
                    Record(epoch=Epoch.get_current_epoch(),
                           day=DayTracker.get_current_day(),
                           being_id=f"{self.id}",
                           event_type="WAR",
                           description=details))
            else:
                if self.war_xp == other_human.war_xp:
                    theft_outcome = random.choices(['theft','war'], weights=[self.theft + 0.1, self.war_xp + 0.1])[0]
                    if theft_outcome == 'theft':
                        self.theft += 1
                        amount = random.randint(0,round(other_human.resources))
                        self.resources += amount
                        other_human.resources -= amount
                        log_instance = Log()
                        details = f"contacted {other_human.id} @ {self.x, self.y}"
                        log_instance.add_record(
                            Record(epoch=Epoch.get_current_epoch(),
                                   day=DayTracker.get_current_day(),
                                   being_id=f"{self.id}",
                                   event_type="STL",
                                   description=details))
                        if other_human.theft > 1:
                            other_human.theft -= 1
                            log_instance = Log()
                            details = f"contacted {self.id} @ {other_human.x, other_human.y}"
                            log_instance.add_record(
                                Record(epoch=Epoch.get_current_epoch(),
                                       day=DayTracker.get_current_day(),
                                       being_id=f"{other_human.id}",
                                       event_type="ROB",
                                       description=details))
                        else:
                            other_human.theft = 0
                    else:
                        self.war_xp += 1  # Gain war experience
                        self.resources += other_human.resources  # Take all resources from the defeated
                        other_human.resources = 0  # The defeated loses all resources
                        other_human.is_zombie = True  # The defeated becomes a zombie
                        self.hh_kd += 1
                        self.h_enc += 1
                        log_instance = Log()
                        details = f"contacted {other_human.id} @ {self.x, self.y}"
                        log_instance.add_record(
                            Record(epoch=Epoch.get_current_epoch(),
                                   day=DayTracker.get_current_day(),
                                   being_id=f"{self.id}",
                                   event_type="WAR",
                                   description=details))

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
                self.resources= 0 # Human becomes a zombie
                # print(f"Being {self.id} (human) starved.")

#-----------------------------------------------------------------
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.beings = []
        self.rmv_beings = 0
        self.occupied_positions = set()

    def add_being(self, being):
        while (being.x, being.y) in self.occupied_positions:  # Check if position is occupied
            # Generate new positions until an unoccupied one is found
            being.x = random.randint(0, self.width - 1)
            being.y = random.randint(0, self.height - 1)
        self.occupied_positions.add((being.x, being.y))  # Mark the new position as occupied
        self.beings.append(being)

    def move_being(self, being):
        dx = random.choice([-1, 0, 1])  # Randomly choose a direction
        dy = random.choice([-1, 0, 1])
        new_x = max(0, min(being.x + dx, self.width - 1))
        new_y = max(0, min(being.y + dy, self.height - 1))

        # Check if the new position is occupied
        if (new_x, new_y) not in self.occupied_positions:
            self.occupied_positions.remove((being.x, being.y))
            self.occupied_positions.add((new_x, new_y))
            being.move(dx, dy, grid=self)

    def simulate_day(self):
        for being in list(self.beings):  # list copy to avoid issues while modifying the list
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

# -----------------------------------------------------------------------------------------


class Record:
    def __init__(self, epoch, day, being_id, event_type, description):
        self.epoch = epoch
        self.day = day
        self.being_id = being_id
        self.event_type = event_type
        self.description = description

    def __repr__(self):
        return (f"Epoch: {self.epoch}, "
                f"Day {self.day}, "
                f"ID:{self.being_id}, "
                f"Type: {self.event_type}, "
                f"Desc: {self.description}")

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
