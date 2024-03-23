def make_group_decision(encounter_type, group_members):
    """Make a decision during an encounter based on group's collective attributes."""
    if encounter_type == 'zombie':
        # Example: decide to fight or flee based on group's collective win_xp and esc_xp
        fight_chance = sum(member.win_xp for member in group_members) / len(group_members)
        flee_chance = sum(member.esc_xp for member in group_members) / len(group_members)
        return 'fight' if fight_chance > flee_chance else 'flee'
    # Additional decision types can be added here

def calculate_average_resources(group_members):
    """Calculate the average resources among a group of beings."""
    total_resources = sum(member.resources for member in group_members)
    return total_resources / len(group_members) if group_members else 0

def merge_groups(group1, group2):
    """Merge two groups into one, combining their members."""
    # Assuming Group class has a method to add members
    for member in group2.members.values():
        group1.add_member(member)
    # Additional logic for handling the merging process, like updating group references for members

# Additional utility functions or classes can be defined here as needed
