class Entity:
    last_id = 0

    def __init__(self, x, y, z):
        Entity.last_id += 1
        self.id = Entity.last_id
        self.x = x
        self.y = y
        self.z = z

    def move(self, dx, dy, dz=0):
        self.x += dx
        self.y += dy
        self.z += dz


class LivingEntity(Entity):
    def __init__(self, x, y, z, health):
        super().__init__(x, y, z)
        self.health = health
        self.is_active = True

    def update_health(self, delta):
        self.health += delta
        if self.health <= 0:
            self.die()

    def die(self):
        self.is_active = False
        # Additional logic for when the entity dies


class Being(LivingEntity):
    def __init__(self, x, y, z, health, grid, is_zombie=False, esc_xp=0, win_xp=0, love_xp=0, war_xp=0, lifespan_z=10):
        super().__init__(x, y, z, health)
        self.grid = grid
        self.is_zombie = is_zombie
        self.esc_xp = esc_xp
        self.win_xp = win_xp
        self.love_xp = love_xp
        self.war_xp = war_xp
        self.lifespan_z = lifespan_z
        self.group = None  # Reference to the group this being belongs to

    # Define specific behaviors for Beings here (encounter, fight, flee, etc.)


class Human(Being):
    def __init__(self, x, y, z, health, grid):
        super().__init__(x, y, z, health, grid)

    # Define human-specific behaviors here


class Zombie(Being):
    def __init__(self, x, y, z, grid, lifespan_z):
        super().__init__(x, y, z, health=0, grid=grid, is_zombie=True, lifespan_z=lifespan_z)

    # Define zombie-specific behaviors here


class Group:
    last_group_id = 0

    def __init__(self):
        Group.last_group_id += 1
        self.group_id = Group.last_group_id
        self.members = {}  # Key: Being ID, Value: Being instance

    def add_member(self, being):
        self.members[being.id] = being
        being.group = self  # Link the being back to this group

    def remove_member(self, being_id):
        if being_id in self.members:
            self.members.pop(being_id).group = None  # Remove from group and unlink the being from this group

    # Additional group-related methods here (e.g., merging groups)
