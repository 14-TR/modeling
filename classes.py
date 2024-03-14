import random

class Being:
    def __init__(self, id, resources, is_zombie=False, esc_xp=0, win_xp=0, love_xp=0, war_xp=0, lifespan=10):
        self.id = id
        self.x = x
        self.y = y
        self.resources = resources
        self.is_zombie = is_zombie
        self.esc_xp = esc_xp
        self.win_xp = win_xp
        self.love_xp = love_xp
        self.war_xp = war_xp
        self.lifespan = lifespan  # Relevant only for zombies

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def encounter(self, other):
        if self.is_zombie:
            self.encounter_as_zombie(other)
        else:
            if other.is_zombie:
                self.encounter_zombie(other)
            else:
                self.encounter_human(other)

    def encounter_as_zombie(self, other):
        if not other.is_zombie:  # Zombie tries to infect human
            other.is_zombie = True  # Human gets infected and becomes a zombie
            self.lifespan += 3  # Zombie's lifespan increases
        # If the other is a zombie, no interaction occurs

    def encounter_zombie(self, zombie):
        # Decide the outcome: escape, win, or get infected
        outcome = random.choices(['escape', 'win', 'infected'], weights=[self.esc_xp, self.win_xp, 1])[0]

        if outcome == 'escape':
            self.esc_xp += 1  # Gain escape experience
        elif outcome == 'win':
            self.win_xp += 1  # Gain win experience
            self.resources += 1  # Gain a small amount of resources
            zombie.lifespan -= 1  # Reduce zombie's lifespan
        else:  # infected
            self.is_zombie = True
            self.lifespan = 10  # Reset lifespan as a zombie

    def encounter_human(self, other_human):
        # Decide the outcome: love or war, ensuring weights are never zero by adding a small value
        outcome = random.choices(['love', 'war'], weights=[self.love_xp + 0.1, self.war_xp + 0.1])[0]

        if outcome == 'love':
            self.love_xp += 1  # Gain love experience
            other_human.love_xp += 1
            avg_resources = (self.resources + other_human.resources) / 2
            self.resources = other_human.resources = avg_resources  # Even out resources
        else:  # war
            if self.war_xp > other_human.war_xp or (self.war_xp == other_human.war_xp and random.choice([True, False])):
                self.war_xp += 1  # Gain war experience
                self.resources += other_human.resources  # Take all resources from the defeated
                other_human.resources = 0  # The defeated loses all resources

    def update_status(self):
        if self.is_zombie:
            self.lifespan -= 1  # Simulate the decay of the zombie
            if self.lifespan <= 0:
                print(f"Being {self.id} (zombie) decayed.")
        else:
            if self.resources > 0:
                self.resources -= 0.5  # Simulate resource consumption for humans
            else:
                print(f"Being {self.id} (human) starved.")

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.beings = []

    def add_being(self, being):
        self.beings.append(being)

    def move_being(self, being, dx, dy):
        dx = random.choice([-1, 0, 1])  # Randomly choose a direction
        dy = random.choice([-1, 0, 1])
        being.x = max(0, min(self.width - 1, being.x + dx))  # Ensure the being stays within the grid
        being.y = max(0, min(self.height - 1, being.y + dy))

    def simulate_day(self):
        for being in self.beings:
            self.move_being(being)
            for other in self.beings:
                if other != being and abs(other.x - being.x) <= 1 and abs(other.y - being.y) <= 1:
                    being.encounter(other)
            being.update_status()