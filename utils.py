import pandas as pd


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

def write_logs_to_dataframes(log_instance):
    # Assuming log_instance is an instance of your Log class containing all the logs

    # Encounter Records
    encounter_records = [{
        'ID': record.id.hex,
        'Epoch': record.epoch,
        'Day': record.day,
        'Being ID': record.being_id,
        'Encounter Type': record.encounter_type,
        'Other Being ID': record.other_being_id,
        'X': record.x,
        'Y': record.y,
        'Z': record.z
    } for record in log_instance.encounter_logs]

    encounter_df = pd.DataFrame(encounter_records)

    # Resource Change Records
    resource_records = [{
        'ID': record.id.hex,
        'Epoch': record.epoch,
        'Day': record.day,
        'Being ID': record.being_id,
        'Resource Change': record.resource_change,
        'Current Resources': record.current_resources,
        'Reason': record.reason,
        'X': record.x,
        'Y': record.y,
        'Z': record.z
    } for record in log_instance.resource_logs]

    resource_df = pd.DataFrame(resource_records)

    # Movement Records - Note the change here to use inherited x, y, z for the end position
    movement_records = [{
        'ID': record.id.hex,
        'Epoch': record.epoch,
        'Day': record.day,
        'Being ID': record.being_id,
        'Start X': record.start_x,
        'Start Y': record.start_y,
        'Start Z': record.start_z,
        'End X': record.x,  # Use inherited x
        'End Y': record.y,  # Use inherited y
        'End Z': record.z   # Use inherited z
    } for record in log_instance.movement_logs]

    movement_df = pd.DataFrame(movement_records)

    # Combine all DataFrames
    # combined_df = pd.concat([encounter_df, resource_df, movement_df], ignore_index=True, sort=False)

    # return encounter_df, resource_df, movement_df, combined_df
    return encounter_df, resource_df, movement_df



def output_to_csv(df, filename):
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
