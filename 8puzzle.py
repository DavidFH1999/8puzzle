import random
import time

# Global variables
state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
state_backup = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
last_indexes = [0, 0]
last_indexes_backup = [0, 0]


# Methods region
# Moves up the specified field's value if possible
def move_up(i):
    swap(i-3, i)


# Returns whether the specified field's value can move up
def can_move_up(i):
    if i > 2 and is_free(i-3) and not was_last_move(i-3, i):
        return True
    return False


# Moves down the specified field's value if possible
def move_down(i):
    swap(i, i+3)


# Returns whether the specified field's value can be moved down
def can_move_down(i):
    if i < 6 and is_free(i+3) and not was_last_move(i, i+3):
        return True
    return False


# Moves the specified field's value to the right if possible
def move_right(i):
    swap(i, i+1)


# Returns whether the specified field's value can move right
def can_move_right(i):
    if i % 3 != 2 and is_free(i+1) and not was_last_move(i, i+1):
        return True
    return False


# Moves the specified field's value to the left
def move_left(i):
    swap(i-1, i)


# Returns whether the specified field's can move left
def can_move_left(i):
    if i % 3 != 0 and is_free(i-1) and not was_last_move(i-1, i):
        return True
    return False


# Returns whether the current state is the goal state
def check():
    return state == goal


# Shuffle the current state to create a random start state
def generate_random_start_state():
    random.shuffle(state)


# Returns whether the specified field is free (0)
def is_free(i):
    return 8 >= i >= 0 == state[i]


# Swaps the specified field's value with the empty field
def swap(i1, i2):
    a, b = state[i1], state[i2]
    state[i1], state[i2] = b, a
    last_indexes[0] = i1
    last_indexes[1] = i2


# Returns true if the current move reverts the last one
def was_last_move(i1, i2):
    return i1 == last_indexes[0] and i2 == last_indexes[1]


# Revert the last move
def revert_last_move():
    swap(last_indexes[0], last_indexes[1])


def print_table():
    table = str(state[0]) + " | " + str(state[1]) + " | " + str(state[2])
    table += "\n---------\n"
    table += str(state[3]) + " | " + str(state[4]) + " | " + str(state[5])
    table += "\n---------\n"
    table += str(state[6]) + " | " + str(state[7]) + " | " + str(state[8]) + "\n"
    print(table)


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
            if j < state[i] != 0:
                inversions += 1
    return inversions

# Uses the get_inversions() function to determine whether the current state is solvable or not
def solvable():
    return get_inversions() % 2 == 0


def get_amount_misplaced_tiles():
    misplaced_tiles = 0
    for i in range(9):
        if state[i] != i:
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
        if can_move_up(i):
            move_up(i)
            amount_misplaced_tiles[0] = get_amount_misplaced_tiles()
            revert_last_move()
        elif can_move_right(i):
            move_right(i)
            amount_misplaced_tiles[1] = get_amount_misplaced_tiles()
            revert_last_move()
        elif can_move_down(i):
            move_down(i)
            amount_misplaced_tiles[2] = get_amount_misplaced_tiles()
            revert_last_move()
        elif can_move_left(i):
            move_left(i)
            amount_misplaced_tiles[3] = get_amount_misplaced_tiles()
            revert_last_move()
        restore_last_indexes()
    return amount_misplaced_tiles


# Algorithm region
def algorithm1():
    count = 0  # The 'count' variable indicates the nodes expanded
    while not check():
        print_table()
        amount_misplaced_tiles = hamming_distance()[:]
        smallest_distance = min(amount_misplaced_tiles)
        if amount_misplaced_tiles[0] == smallest_distance:
            for i in range(9):
                if can_move_up(i):
                    move_up(i)
                    break
        elif amount_misplaced_tiles[1] == smallest_distance:
            for i in range(9):
                if can_move_right(i):
                    move_right(i)
                    break
        elif amount_misplaced_tiles[2] == smallest_distance:
            for i in range(9):
                if can_move_down(i):
                    move_down(i)
                    break
        else:
            for i in range(9):
                if can_move_left(i):
                    move_left(i)
                    break
        count += 1
    return count


def algorithm2():
    count = 0
    while not check():
        # Insert algorithm here
        count += 1
    return count


if __name__ == '__main__':
    generate_random_start_state()  # Initiate array
    #state = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    if not solvable():
        print_table()
        print("This given state cannot be solved since the amount of inversions is odd!")
        exit()
    # Save random start state to a backup to compare the algorithms with the same start state used
    state_backup = state[:]

    # Algorithm 1
    start = time.time()
    count1 = algorithm1()
    total_time1 = round(time.time() - start, 3)
    print("ALGORITHM_1 took " + str(total_time1) + " seconds. " + str(count1) + " nodes were expanded.")
    print_table()

    # Algorithm 2
    # Reset state to the defined random beginner start state again for a better comparison of the algorithms
    state = state_backup[:]
    start = time.time()
    # count2 = algorithm2()
    total_time_2 = round(time.time() - start, 3)
    # print("ALGORITHM_2 took " + str(total_time_2) + " seconds. " + str(count2) + " nodes were expanded.")

