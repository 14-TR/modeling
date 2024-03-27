class GroupManager:
    def __init__(self):
        self.groups = []
        self.group_logs = []

    def create_group(self, members, epoch, start_day):
        new_group = Group(members)
        self.groups.append(new_group)
        log_record = GroupLogRecord(new_group.id, epoch, start_day)
        new_group.log = log_record
        self.group_logs.append(log_record)
        return new_group

    def move_group(self, group, direction):
        dx, dy = direction
        for member in group.members:
            new_x = max(0, min(member.x + dx, member.grid.width - 1))
            new_y = max(0, min(member.y + dy, member.grid.height - 1))
            member.x, member.y = new_x, new_y

    def group_encounter(self, group1, group2):
        pass

    # Logic for group vs. group encounters

    def individual_encounter(self, group, individual):
        pass

    # Logic for encounters between a group member and an individual not in a group

    def merge_groups(self, group1, group2):
        # Merge group2 into group1 and dissolve group2
        for member in group2.members:
            group1.add_member(member)  # This updates the member's group reference
        self.dissolve_group(group2)

    def dissolve_group(self, group):
        # Remove the group from the manager's list and clear its members' group reference
        for member in group.members:
            member.group = None
        self.groups.remove(group)


class Group:
    last_id = 0

    def __init__(self, members=None):
        Group.last_id += 1
        self.id = Group.last_id
        self.members = members if members is not None else []

    def calculate_average_resources(self):
        if not self.members:
            return None  # No average if the group has no members

        total_resources = sum(member.resources for member in self.members)
        return total_resources / len(self.members)

    def add_member(self, being):
        self.members.append(being)
        being.group = self
        self.log.members_added += 1

    def remove_member(self, being):
        self.members.remove(being)
        being.group = None
        self.log.members_lost += 1

        # If the group is now empty, consider dissolving it or taking other actions
        if not self.members:
            # Call a method to dissolve the group or handle the empty group scenario
            pass

    def close_group(self, end_day):
        self.log.end_day = end_day

    def calculate_centroid(self):
        if not self.members:
            return None  # Return None if the group has no members

        avg_x = sum(member.x for member in self.members) / len(self.members)
        avg_y = sum(member.y for member in self.members) / len(self.members)
        return avg_x, avg_y

    def find_closest_resource_point(self, grid):
        centroid = self.calculate_centroid()
        if centroid is None:
            return None

        closest_point = None
        min_distance = float('inf')
        for point in grid.resource_points:
            distance = ((centroid[0] - point[0]) ** 2 + (centroid[1] - point[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_point = point

        return closest_point

    def calculate_average_distance_to_point(self, point):
        total_distance = 0
        for member in self.members:
            distance = ((member.x - point[0]) ** 2 + (member.y - point[1]) ** 2) ** 0.5
            total_distance += distance
        return total_distance / len(self.members)

    def move_group_towards_closest_resource(self, grid, resource_threshold):
        if self.calculate_average_resources() > resource_threshold:
            return  # The group's resources are sufficient, no need to move towards resources

        closest_resource_point = self.find_closest_resource_point(grid)
        if closest_resource_point is None:
            return  # No movement if no resource points are available

        # Move each member towards the closest resource point
        for member in self.members:
            dx, dy = member.move_towards_resource_point([closest_resource_point])
            member.move(dx, dy, grid)

        # After moving, check if any member has reached the resource point
        for member in self.members:
            if (member.x, member.y) == closest_resource_point:
                self.replenish_and_distribute_resources(member)
                break

    def replenish_and_distribute_resources(self, collector):
        # The collector replenishes their resources up to the maximum of 10
        replenished_amount = min(20 - collector.resources, 20)  # Assuming 20 is the max replenishable amount
        collector.resources += replenished_amount

        # Distribute resources evenly among group members
        self.distribute_resources()

    def distribute_resources(self):
        total_resources = sum(member.resources for member in self.members)
        average_resources = total_resources / len(self.members)

        for member in self.members:
            member.resources = average_resources  # Update each member

    # add move and resource logging for all of these and encounter logging


class GroupLogRecord:
    def __init__(self, group_id, epoch, start_day, end_day=None, members_added=0, members_lost=0):
        self.group_id = group_id
        self.epoch = epoch
        self.start_day = start_day
        self.end_day = end_day
        self.members_added = members_added
        self.members_lost = members_lost


class GroupLog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GroupLog, cls).__new__(cls)
            cls._instance.records = []
        return cls._instance

    def add_record(self, record):
        self.records.append(record)
