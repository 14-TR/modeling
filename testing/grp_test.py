from archive.classes import Grid, Being


def main():
    # Initialize the grid
    grid = Grid(width=10, height=10)

    # Create human beings and a zombie
    human1 = Being(x=1, y=1, z=0, resources=10, win_xp=0, grid=grid, is_zombie=False)
    human2 = Being(x=2, y=2, z=0, resources=10, win_xp=2, grid=grid, is_zombie=False)
    zombie = Being(x=1, y=1, z=0, resources=0, grid=grid, is_zombie=True)

    # Add beings to the grid
    grid.add_being(human1)
    grid.add_being(human2)
    grid.add_being(zombie)

    # Humans form a group
    human1.join_group(human2)

    # Prepare group members list for the encounter
    group_members = [grid.beings[member_id] for member_id in human1.grp_mbrs] + [human1]

    # Print initial states
    print("Before the encounter:")
    print(f"Human1 resources: {human1.resources}, win_xp: {human1.win_xp}, group_members: {human1.grp_mbrs}")
    print(f"Human2 resources: {human2.resources}, win_xp: {human2.win_xp}, group_members: {human2.grp_mbrs}")
    print(f"Zombie is_active: {zombie.is_active}")

    # Simulate the encounter where humans fight the zombie as a group
    human1.fight_zombie(zombie, group_members)

    # Print outcomes to verify group functionality
    print("\nAfter the encounter:")
    print(f"Human1 resources: {human1.resources}, win_xp: {human1.win_xp}, group_members: {human1.grp_mbrs}")
    print(f"Human2 resources: {human2.resources}, win_xp: {human2.win_xp}, group_members: {human2.grp_mbrs}")
    print(f"Zombie is_active: {zombie.is_active}")

if __name__ == "__main__":
    main()