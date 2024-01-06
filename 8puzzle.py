import random
import time

# Global variables
cur_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
state_backup = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
last_indexes = [0, 0]
last_indexes_backup = [0, 0]


# region Methods
# Moves up the specified field's value if possible
def move_up(i):
    if i > 2 and is_free(i - 3) and not was_last_move(i - 3, i):
        swap(i - 3, i)
        return True


# Moves down the specified field's value if possible
def move_down(i):
    if i < 6 and is_free(i + 3) and not was_last_move(i, i + 3):
        swap(i, i + 3)
        return True


# Moves the specified field's value to the right if possible
def move_right(i):
    if i % 3 != 2 and is_free(i + 1) and not was_last_move(i, i + 1):
        swap(i, i + 1)
        return True


# Moves the specified field's value to the left
def move_left(i):
    if i % 3 != 0 and is_free(i - 1) and not was_last_move(i - 1, i):
        swap(i - 1, i)
        return True


# endregion

# Returns whether the current state is the goal state
def check():
    return cur_state == goal


# Returns whether the specified field is free (0)
def is_free(i):
    return 8 >= i >= 0 == cur_state[i]


# Swaps the specified field's value with the empty field
def swap(i1, i2):
    a, b = cur_state[i1], cur_state[i2]
    cur_state[i1], cur_state[i2] = b, a
    last_indexes[0] = i1
    last_indexes[1] = i2


# Returns true if the current move reverts the last one
def was_last_move(i1, i2):
    return i1 == last_indexes[0] and i2 == last_indexes[1]


# Revert the last move
def revert_last_move():
    swap(last_indexes[0], last_indexes[1])


'''
Any pair of tiles i and j, where i < j, but i appears after j in the 3*3 field is considered an inversion
If there is an odd number of inversions in the current state, the 8-puzzle becomes unsolvable
Since each (legal) move changes the amount of inversions by an even number (0, 2), the state is unsolvable when an
odd amount of inversions is found because the amount of inversions in the goal state is 0
'''


def get_inversions():
    inversions = 0
    for i in range(9):
        for j in range(i, 9):
            if j < cur_state[i] != 0:
                inversions += 1
    return inversions


# Uses the get_inversions() function to determine whether the current state is solvable or not
def solvable():
    return get_inversions() % 2 == 0


def get_amount_misplaced_tiles():
    misplaced_tiles = 0
    for i in range(9):
        if cur_state[i] != goal[i] and cur_state[i] != 0:  # Skip the blank/0 tile
            misplaced_tiles += 1
    return misplaced_tiles


def save_last_indexes():
    last_indexes_backup[0], last_indexes_backup[1] = last_indexes[0], last_indexes[1]


def restore_last_indexes():
    last_indexes[0], last_indexes[1] = last_indexes_backup[0], last_indexes_backup[1]


'''
Checks all available legal moves and calculates the hamming distance
The hamming distance is incremented by one for each tile that sits on an incorrect position
'''


def hamming_distance():
    amount_misplaced_tiles = [10, 10, 10, 10]
    for i in range(9):
        save_last_indexes()
        if move_up(i):
            move_up(i)
            amount_misplaced_tiles[0] = get_amount_misplaced_tiles()
            revert_last_move()
        elif move_right(i):
            move_right(i)
            amount_misplaced_tiles[1] = get_amount_misplaced_tiles()
            revert_last_move()
        elif move_down(i):
            move_down(i)
            amount_misplaced_tiles[2] = get_amount_misplaced_tiles()
            revert_last_move()
        elif move_left(i):
            move_left(i)
            amount_misplaced_tiles[3] = get_amount_misplaced_tiles()
            revert_last_move()
        restore_last_indexes()
    return amount_misplaced_tiles


# Algorithm region
def hamming():
    count = 0  # The 'count' variable indicates the nodes expanded
    while not check():
        amount_misplaced_tiles = hamming_distance()[:]
        smallest_distance = min(amount_misplaced_tiles)
        if amount_misplaced_tiles[0] == smallest_distance:
            for i in range(9):
                if move_up(i):
                    break
        elif amount_misplaced_tiles[1] == smallest_distance:
            for i in range(9):
                if move_right(i):
                    break
        elif amount_misplaced_tiles[2] == smallest_distance:
            for i in range(9):
                if move_down(i):
                    break
        else:
            for i in range(9):
                if move_left(i):
                    break
        count += 1
    return count


# Calculate Manhattan distance
def manhattan_distance():
    total_distance = 0
    for i in range(9):
        if cur_state[i] == 0:
            continue  # Skip the blank tile
        # Calculate the positions (x,y) for current and goal positions
        current_position = (i // 3, i % 3)  # div mod(i, 3) gives (quotient, remainder)
        goal_position = (cur_state[i] // 3, cur_state[i] % 3)  # Number's correct position
        # Add Manhattan distance for this tile
        total_distance += abs(current_position[0] - goal_position[0]) + abs(current_position[1] - goal_position[1])
    return total_distance


def manhattan_distance_single_tile(current_index, value):
    # Calculate the positions (x,y) for current and goal positions
    current_position = (current_index // 3, current_index % 3)
    goal_position = (value // 3, value % 3)  # Number's correct position
    # Calculate and return Manhattan distance for this tile
    return abs(current_position[0] - goal_position[0]) + abs(current_position[1] - goal_position[1])


def total_manhattan_distance():
    total_distance = 0
    for index, value in enumerate(cur_state):
        if value == 0:
            continue  # Skip the blank tile
        total_distance += manhattan_distance_single_tile(index, value)
    return total_distance


# Algorithm 2 implementation using Manhattan Distance
def manhattan():
    count = 0
    while not check():
        best_move = None
        lowest_distance = None

        # Save current state to revert after checking moves
        state_before_move = cur_state[:]

        # Check each possible move and calculate the Manhattan distance
        for i in range(9):
            if move_up(i):
                distance = total_manhattan_distance()
                if lowest_distance is None or distance < lowest_distance:
                    lowest_distance = distance
                    best_move = ('up', i)
                cur_state[:] = state_before_move  # Revert to state before move

            if move_right(i):
                distance = total_manhattan_distance()
                if lowest_distance is None or distance < lowest_distance:
                    lowest_distance = distance
                    best_move = ('right', i)
                cur_state[:] = state_before_move

            if move_down(i):
                distance = total_manhattan_distance()
                if lowest_distance is None or distance < lowest_distance:
                    lowest_distance = distance
                    best_move = ('down', i)
                cur_state[:] = state_before_move

            if move_left(i):
                distance = total_manhattan_distance()
                if lowest_distance is None or distance < lowest_distance:
                    lowest_distance = distance
                    best_move = ('left', i)
                cur_state[:] = state_before_move

        # Perform the best move
        if best_move:
            direction, index = best_move
            if direction == 'up':
                move_up(index)
            elif direction == 'right':
                move_right(index)
            elif direction == 'down':
                move_down(index)
            elif direction == 'left':
                move_left(index)

        count += 1  # Increment the number of moves made

    return count


if __name__ == '__main__':
    solvable_puzzles = []
    while len(solvable_puzzles) < 100:
        # generate a random puzzle
        random.shuffle(cur_state)
        # check if its solvable
        if solvable():
            # If solvable, store it for later use
            solvable_puzzles.append(cur_state[:])  # Make sure to append a copy of the state

    # Now you have 100 solvable puzzles stored in solvable_puzzles
    # Next, run Algorithm 1 and Algorithm 2 on each puzzle and record the results

    for puzzle in solvable_puzzles:
        # Set the current state to the puzzle
        cur_state = puzzle

        # Run Algorithm 1
        # Record nodes expanded and time taken

        # Reset the current state to the puzzle again
        # cur_state = puzzle

        # Run Algorithm 2
        # Record nodes expanded and time taken

        # Algorithm 1
        start = time.time()
        count1 = hamming()
        total_time1 = round(time.time() - start, 3)
        print("ALGORITHM_1 took " + str(total_time1) + " seconds. " + str(count1) + " nodes were expanded.")

        # Algorithm 2
        # Reset state to the defined random beginner start state again for a better comparison of the algorithms
        # cur_state = state_backup[:]
        start = time.time()
        # count2 = algorithm2()
        total_time_2 = round(time.time() - start, 3)
        # print("ALGORITHM_2 took " + str(total_time_2) + " seconds. " + str(count2) + " nodes were expanded.")
