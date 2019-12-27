if game_state == GameStates.PLAYERS_TURN:
    if not game_map.is_blocked(destination_x, destination_y):
        # If the current direction the player is travelling is not blocked, continue that direction
        player.move(dx, dy)
    # if the current direction is blocked:
    elif player.direction is game_map.is_blocked(destination_x, destination_y):
        # Check the 8 (minus previous location) space area around player for non blocked space.
        if check Rect(player.x - 1, player.y - 1, w + 2, h + 2)(not player.x and player.y and player.(px, py)) for not game_map.is_blocked():
            if 1 space is found:
                # If only one space is found, move that direction
                player.move(dx, dy)
            elif > 1 space is found:
                # If more than one space is found, let the player chose the direction.
                wait_for_key_event(player select course)
                player.move(dx, dy)
            elif 0 spaces found:
                # Move the player back to the previous location and keep moving
                player.move(px, py)
