######################################################################
# WRITER : Matanel Pataki
# DESCRIPTION: A program that solves nanograms
######################################################################
import copy
import math

WHITE = 0
BLACK = 1
UNFILLED = -1
#  for nonogram's constraints:
ROWS = 0
COLUMNS = 1


def can_place_block(cur_row, block_len, row_index):
    """
    This function testing to see if it's possible to place the block in the
    current position.
    :param cur_row: a list, The current row.
    :param block_len:  an integer, the length of the block to place.
    :param row_index: and integer, the current index of the row to test.
    :return: True if it's possible to place the block, False otherwise.
    """
    # check that there is place for the block
    if row_index + block_len > len(cur_row):
        return False
    # check if all cells in wanted block range are free or black
    for i in range(row_index, row_index + block_len):
        if cur_row[i] == WHITE:
            return False
    # check if block is at the end of the row, or that there is space for white
    if row_index + block_len != len(cur_row):
        if cur_row[row_index + block_len] == BLACK:
            return False
    return True


def place_block(row, block_len, row_index):
    """
    This function is placing the block by changing the values of the correct
    cells in the row to blacks.
    :param row: a list, The current row to change.
    :param block_len: an integer, the length of the block to place.
    :param row_index: and integer, the current index of the row to change from.
    :return: The row after being changed.
    """
    for i in range(row_index, row_index + block_len):
        row[i] = BLACK
    if row_index + block_len < len(row):
        row[row_index + block_len] = WHITE
    return row


def fill_row_variations(row_variations, cur_row, blocks, row_index,
                        blocks_index):
    """
    This function fills the row variations by using backtracking. Trying to
    fill the unfilled cell with white, and then black and saving the valid
    results.
    :param row_variations: a list of all the variations so far.
    :param cur_row: a list, the current row.
    :param blocks: a list, the blocks to fill.
    :param row_index: an integer, the current index tested.
    :param blocks_index: an integer, the current index of the block tested.
    :return: None
    """
    if base_case(blocks, blocks_index, cur_row, row_index, row_variations):
        return
    row_index, is_successful = \
        advance_until_placement_is_possible(blocks, blocks_index, cur_row,
                                            row_index)
    if not is_successful or row_index == len(cur_row):
        return
    fill_row_variations_without_placement(blocks, blocks_index, cur_row,
                                          row_index, row_variations)
    fill_row_variations_with_placement(blocks, blocks_index, cur_row,
                                       row_index, row_variations)


def fill_row_variations_without_placement(blocks, blocks_index, cur_row,
                                          row_index, row_variations):
    """
    This function fills the row without placing black instead of the unfilled
    cells of the row.
    :param blocks: a list, the blocks to fill.
    :param blocks_index: an integer, the current index of the block tested.
    :param cur_row: a list, the current row.
    :param row_index: an integer, the current index tested.
    :param row_variations: a list of all the variations so far.
    :return: None
    """
    if cur_row[row_index] != BLACK:
        cur_row_without_placement = cur_row[:]
        if cur_row_without_placement[row_index] != BLACK:
            cur_row_without_placement[row_index] = WHITE
        else:
            cur_row_without_placement[row_index] = BLACK
        fill_row_variations(row_variations, cur_row_without_placement, blocks,
                            row_index + 1, blocks_index)


def fill_row_variations_with_placement(blocks, blocks_index, cur_row,
                                       row_index, row_variations):
    """
    This function fills the row with placing blacks instead of the unfilled
    cells of the row.
    :param blocks: a list, the blocks to fill.
    :param blocks_index: an integer, the current index of the block tested.
    :param cur_row: a list, the current row.
    :param row_index: an integer, the current index tested.
    :param row_variations: a list of all the variations so far.
    :return: None
    """
    cur_row_after_placement = place_block(cur_row[:], blocks[blocks_index],
                                          row_index)
    fill_row_variations(row_variations, cur_row_after_placement, blocks,
                        row_index + blocks[blocks_index] + 1, blocks_index + 1)


def advance_until_placement_is_possible(blocks, blocks_index, cur_row,
                                        row_index):
    """
    This function is going through the current row and checking to see if it
    is possible to place the block in the current row index tested.
    :param blocks: a list, the blocks to fill.
    :param blocks_index: an integer, the current index of the block tested.
    :param cur_row: a list, the current row.
    :param row_index: an integer, the current index tested.
    :return: a tuple, the index row from witch to fill the blocks, and a
                        boolean indicating if it is even possible.
    """
    while (not can_place_block(cur_row, blocks[blocks_index],
                               row_index)) and row_index < len(cur_row):
        if cur_row[row_index] == UNFILLED:
            cur_row[row_index] = WHITE
        if cur_row[row_index] == BLACK:
            # can't place block when current cell is black
            return row_index, False  # return
        row_index += 1
    return row_index, True


def get_row_variations(row, blocks):
    """
    This function is taking all the possible variations to fill a given row
    with given blocks. And then returns each variation as a list within the
    main list of variations.
    :param row: A list, the given row to fill.
    :param blocks: A list, the given blocks to place within the row.
    :return: a 2 dimensional list, all the variations of the filled row.
    """
    row_variations = []
    fill_row_variations(row_variations, row[:], blocks, 0, 0)  # backtracking
    return row_variations


def base_case(blocks, blocks_index, cur_row, row_index, row_variations):
    """
    Checks for base case and deals appropriately
    :param blocks: list of block sizes
    :param blocks_index: the current block to fill
    :param cur_row: the current state of the row
    :param row_index: the current cell in the row to fill from
    :param row_variations: list of all possible row solutions
    :return: True if base case, else False
    """
    if row_index >= len(cur_row) and blocks_index < len(blocks):
        return True
    if blocks_index >= len(blocks):
        for i in range(row_index, len(cur_row)):
            if cur_row[i] == BLACK:
                return True
            cur_row[i] = WHITE
        row_variations.append(cur_row[:])
        return True
    return False


def get_intersection_row(rows):
    """
    This function gets the intersection row of a given lists so that if all the
    values in the same cell's index in the given lists are the same, the
    intersection will also have that value in that cell's index.
    In case there are a value of -1 in one list's cell and 1 in another list,
    the intersection row will get -1 in the same index. see "Notes" above for
    more info.
    :param rows: a 2 dimensional list, the rows to intersect together.
    :return: a list, the intersection_row
    """
    intersection_row = [-1] * len(rows[0]) if len(rows) != 0 else []
    for i in range(len(intersection_row)):
        all_black = True
        all_white = True
        for row in rows:
            if row[i] != BLACK:
                all_black = False
            if row[i] != WHITE:
                all_white = False
        if all_black:
            intersection_row[i] = BLACK
        if all_white:
            intersection_row[i] = WHITE
    return intersection_row


def create_empty_grid(num_of_rows, num_of_columns):
    """
    This function creates an empty list full of -1.
    :param num_of_rows: integer.
    :param num_of_columns: integer.
    :return: 2d list. the created grid.
    """
    grid = []
    row = [-1] * num_of_rows
    for i in range(num_of_columns):
        grid.append(row)
    return grid


def get_grid_row(grid, i):
    """
    This function returns the row specified.
    :param grid: 2d list. The grid to extract from.
    :param i: integer. The index of the wanted row.
    :return: a list. The row requested.
    """
    return grid[i]


def get_grid_column(grid, i):
    """
    This function returns the column specified.
    :param grid: 2d list. The grid to extract from.
    :param i: integer. The index of the wanted column.
    :return: a list. The column requested.
    """
    return [sub[i] for sub in grid]


def is_unfilled_in_grid(grid):
    """
    This function checking to see if there is still an unfilled cell in the
    grid (-1).
    :param grid: 2d list. the grid to search in.
    :return: True if there is unfilled cell, False otherwise
    """
    for row in grid:
        if UNFILLED in row:
            return True
    return False


def solve_rows_successfully(constraint, grid, for_columns):
    """
    This function is updating the grid by looking trough each row and its
    constraint, and then the same for each column.
    :param constraint: a list, the constraint to account for.
    :param grid: 2d list, the grid to update.
    :param for_columns: boolean, indicating if rows of columns are updating.
    :return: True, if all the grid updated successfully, False otherwise.
    """
    for i in range(len(constraint)):
        cur_row = get_grid_row(grid, i) if not for_columns \
            else get_grid_column(grid, i)
        if UNFILLED in cur_row or len(cur_row) <= 1:
            row_variants = get_row_variations(cur_row, constraint[i])
            if not for_columns:
                update_grid_row(grid, i, row_variants)
            else:
                update_grid_column(grid, i, row_variants)
            if not row_variants:  # no possible solution
                return False
    return True


def update_grid(constraints, grid):
    """
    This function will update the grid by updating the rows and columns.
    It will run in a while loop until there and no -1 left in the grid or if
    the grid is unsolvable.
    :param constraints: 3d list, the constraints to account for the grid.
    :param grid: 2d list, the current grid updating.
    :return: 2d list, the grid after being updated. None if it is unsolvable.
    """
    while is_unfilled_in_grid(grid):
        grid_copy = grid[:]
        if not solve_rows_successfully(constraints[ROWS], grid, False) or \
                not solve_rows_successfully(constraints[COLUMNS], grid, True):
            return None
        if grid_copy == grid:  # in case the grid is not updating anymore
            return grid
    return grid


def solve_easy_nonogram(constraints):
    """
    This function solves a nonogram that have only 1 solution. if there are
    more than 1 solution it will solve it untill it can't, leaving -1 in the
    unsolved cells.
    :param constraints: 3d list, the constraints to account for the nonogram.
    :return: a 2d list, the solved nonogram. None if unsolvable.
    """
    grid = create_empty_grid(len(constraints[COLUMNS]),
                             len((constraints[ROWS])))
    return update_grid(constraints, grid)


def update_grid_row(grid, i, row_variants):
    """
    This function is updating the row specified.
    :param grid: 2d list, the current grid.
    :param i: integer, the current index or the row.
    :param row_variants: 2d list, all the variants possible to fill the row.
    :return: None.
    """
    grid[i] = get_intersection_row(row_variants)


def update_grid_column(grid, i, column_variants):
    """
    This function is updating the column specified.
    :param grid: 2d list, the current grid.
    :param i: integer, the current index or the column.
    :param column_variants: 2d list, all the variants possible to fill.
    :return: None.
    """
    column_to_update = get_intersection_row(column_variants)
    for j in range(len(column_to_update)):
        grid[j][i] = column_to_update[j]


def get_unfilled_index(grid):
    """
    This function is going through the grid and returns the first unfilled cell
    :param grid: 2d list, the current grid to go through.
    :return: a tuple, the index of the row and the column to extract the value.
    """
    for row in range(len(grid)):
        for i in range(len(grid[row])):
            if grid[row][i] == UNFILLED:
                return row, i


def fill_index_with_placement(unfilled_index, grid, constraints,
                              all_grid_options):
    """
    This function is getting witch cell to fill and then fill in with 1.
    :param unfilled_index: a tuple, the index of the row and the column.
    :param grid: 2d list, the current grid.
    :param constraints: 3d list, the constraints to account for the nonogram.
    :param all_grid_options: 3d list, all possible solutions for the nonogram.
    :return: None.
    """
    grid[unfilled_index[0]][unfilled_index[1]] = BLACK
    _helper_solve_nonogram(grid, constraints, all_grid_options)


def fill_index_without_placement(unfilled_index, grid, constraints,
                                 all_grid_options):
    """
    This function is getting witch cell to fill and then fill in with 0.
    :param unfilled_index: a tuple, the index of the row and the column.
    :param grid: 2d list, the current grid.
    :param constraints: 3d list, the constraints to account for the nonogram.
    :param all_grid_options: 3d list, all possible solutions for the nonogram.
    :return: None.
    """
    grid[unfilled_index[0]][unfilled_index[1]] = WHITE
    _helper_solve_nonogram(grid, constraints, all_grid_options)


def _helper_solve_nonogram(grid, constraints, all_grid_options):
    """
    This function solves the nonogram by using backtracking. it will collect
    all possible solutions for the nonogram. Getting all possible variations
    to fill the grid. by using the function from question 3, and each time
    changing 1 value that is unfilled, and then running through that function
    again as a base case, we will get all possible solutions.
    :param grid: 2d list, the current grid.
    :param constraints: 3d list, the constraints to account for the nonogram.
    :param all_grid_options: 3d list, all possible solutions for the nonogram.
    :return: 3d list, all possible solutions for the nonogram.
    """
    grid_option = update_grid(constraints, grid)
    if grid_option is None:
        return
    elif not is_unfilled_in_grid(grid_option):
        all_grid_options.append(grid_option[:])
        return
    if is_unfilled_in_grid(grid_option):
        unfilled_index = get_unfilled_index(grid_option)
        fill_index_with_placement(unfilled_index, copy.deepcopy(grid_option),
                                  constraints, all_grid_options)
        fill_index_without_placement(unfilled_index,
                                     copy.deepcopy(grid_option), constraints,
                                     all_grid_options)
    return all_grid_options


def solve_nonogram(constraints):
    """
    This function gets a list of constraints for both the rows and the columns
    of a nonogram, then returns all possible solution for said nonogram.
    :param constraints: 3d list, the constraints to account for the nonogram.
    :return: 3d list, all possible solutions for the nonogram. [] if unsolvable
    """
    all_grid_options = []
    grid = solve_easy_nonogram(constraints)
    if not grid:
        return []
    if not is_unfilled_in_grid(grid):  # only one possible solution
        all_grid_options.append(grid)
        return all_grid_options
    return _helper_solve_nonogram(grid, constraints, all_grid_options)


def count_row_variations(length, blocks):
    """
    This function returns the amount of  all possible variations there are to
    fill a certain row with certain blocks. By using the a combinatorial
    formula: n choose k.
    :param length: integer, the length of the row.
    :param blocks: a list of integers, representing the blocks to fill.
    :return: an integer, the amount of variations to fill the row.
    """
    n = length - sum(blocks) + 1
    if 0 <= len(blocks) <= n:
        return math.factorial(n) // (math.factorial((n - len(blocks))) *
                                     math.factorial(len(blocks)))
    return 0
