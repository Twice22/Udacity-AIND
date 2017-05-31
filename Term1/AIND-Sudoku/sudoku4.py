test = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

def prod(a, b):
    return [s+t for (s,t) in zip(a,b)]

boxes = cross(rows, cols)
#print(boxes)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
cross = [prod(rs, cs) for (rs,cs) in zip((rows, rows),(cols, cols[::-1]))]
diags = dict((u, set(s)) for s in cross for u in s)

#print(unitlist)
#print(units['A1'])

T1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8', 'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3':'1', 'G2': '8', 'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5' : '5', 'C9': '1', 'G9': '5', 'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5':  '9', 'A4': '2357', 'A7': '27', 'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23',  'E6': '579', 'C7': '9', 'C6': '6', 'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8',  'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2', 'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '12 35', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9', 'D2': '1', 'H1': '4', 'H6': ' 17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27', 'B5': '1', 'B6': '8', 'B7' : '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279', 'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
T2 = {'A1': '23', 'A2': '4', 'A3': '7', 'A4': '6', 'A5': '8', 'A6': '5', 'A7': '23', 'A8': '9', 'A9': '1', 'B1': '6', 'B2': '9', 'B3': '8', 'B4': '4', 'B5': '37', 'B 6': '1', 'B7': '237', 'B8': '5', 'B9': '237', 'C1': '23', 'C2': '5', 'C3': '1', 'C4': '23', 'C5': '379', 'C6': '2379', 'C7': '8', 'C8': '6', 'C9': '4', 'D1': '8 ', 'D2': '17', 'D3': '9', 'D4': '1235', 'D5': '6', 'D6': '237', 'D7': '4', 'D8':  '27', 'D9': '2357', 'E1': '5', 'E2': '6', 'E3': '2', 'E4': '8', 'E5': '347', 'E6': '347', 'E7': '37', 'E8': '1', 'E9': '9', 'F1': '4', 'F2': '17', 'F3': '3', ' F4': '125', 'F5': '579', 'F6': '279', 'F7': '6', 'F8': '8', 'F9': '257', 'G1': ' 1', 'G2': '8', 'G3': '6', 'G4': '35', 'G5': '345', 'G6': '34', 'G7': '9', 'G8': '27', 'G9': '27', 'H1': '7', 'H2': '2', 'H3': '4', 'H4': '9', 'H5': '1', 'H6': ' 8', 'H7': '5', 'H8': '3', 'H9': '6', 'I1': '9', 'I2': '3', 'I3': '5', 'I4': '7',  'I5': '2', 'I6': '6', 'I7': '1', 'I8': '4', 'I9': '8'}


def grid_values(grid):
	g = ["123456789" if c=='.' else c for c in grid]
	assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
	return dict(zip(boxes, g))


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

my_test = grid_values(test)
#display(my_test)
def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    #display(values)
    #print("\n")
    #print(solved_values)
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')

        # diagonal
        if box in diags:
            for d in diags[box]:
                if d != box:
                    values[d] = values[d].replace(digit, '')
    return values

#print(peers)
vanish = eliminate(my_test)
#display(vanish)

display(T1)
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #display(values)
    
    for col in unitlist:
        val_col = [values[c] for c in col]
        twins = [col[p] for p, v in enumerate(val_col) if val_col.count(v) == 2 and len(v) == 2]
        if twins:
            val_to_remove = values[twins[0]]
            for v in col:
                if v not in twins:
                    for digit in val_to_remove:
                        values[v] = values[v].replace(digit, '')
    #print("\nAFTTTTTER : \n")
    #display(values)

    return values

#res = naked_twins(T1)
#print('\n')
#display(res)

vv = {'B5': '47', 'C2': '257', 'H3': '47', 'I9': '2467', 'G8': '1478', 'C4': '8', 'B8': '278', 'C1': '25', 'G1': '134', 'H1': '8', 'D4': '1', 'A3': '3', 'A6': '147', 'B2': '24678', 'I1': '46', 'D3': '8', 'G4': '6', 'D9': '34567', 'I6': '47', 'I8': '24678', 'A7': '6', 'E9': '8', 'G6': '9', 'H8': '1467', 'E1': '7', 'E5': '34569', 'C8': '23579', 'H6': '3', 'F7': '2', 'E4': '459', 'I2': '4679', 'G3': '2', 'F6': '8', 'D2': '345', 'I4': '4', 'D8': '34567', 'C7': '4', 'B3': '47', 'C3': '1', 'E6': '4', 'A4': '49', 'C5': '79', 'G5': '478', 'F3': '6', 'F9': '345', 'G9': '47', 'C6': '6', 'E8': '13456', 'H2': '1467', 'A5': '2', 'E3': '49', 'C9': '2357', 'H9': '9', 'B6': '5', 'B9': '1', 'F2': '13459', 'G2': '1347', 'I7': '3', 'I5': '1', 'E7': '1', 'A9': '57', 'A8': '5789', 'A1': '45', 'H7': '17', 'F5': '3459', 'H4': '2', 'B4': '3', 'G7': '5', 'D5': '3456', 'H5': '457', 'E2': '123459', 'D6': '2', 'B1': '9', 'F4': '7', 'F1': '1345', 'D7': '9', 'I3': '5', 'A2': '4578', 'F8': '1345', 'D1': '345', 'B7': '78'}
#print("BEFORE : \n")
#display(vv)

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here

    for unit in unitlist:
        for digit in '123456789':
        	nb = "".join([values[v] for v in unit if len(values[v]) > 1])
        	places = [v for v in unit if nb.count(digit)==1 and digit in values[v]]
        	if len(places) == 1:
        		values[places[0]] = digit
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        eliminate(values)

        # Your code here: Use the Only Choice Strategy
        only_choice(values)

        naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#other = eliminate(grid_values(grid2))
#display(other)

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    #print("\n")
    #display(values)
    #reduce_puzzle(values)
    #print("lll\n")
    #display(values)
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    

#fnfn = search(other)
#print("\n")
#display(fnfn)

diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
sud = grid_values(diag_sudoku_grid)
display(sud)
print("\n")
tt = search(sud)
display(tt)

solved_diag_sudoku = {'G7': '8', 'G6': '9', 'G5': '7', 'G4': '3', 'G3': '2', 'G2': '4', 'G1': '6', 'G9': '5',
                          'G8': '1', 'C9': '6', 'C8': '7', 'C3': '1', 'C2': '9', 'C1': '4', 'C7': '5', 'C6': '3',
                          'C5': '2', 'C4': '8', 'E5': '9', 'E4': '1', 'F1': '1', 'F2': '2', 'F3': '9', 'F4': '6',
                          'F5': '5', 'F6': '7', 'F7': '4', 'F8': '3', 'F9': '8', 'B4': '7', 'B5': '1', 'B6': '6',
                          'B7': '2', 'B1': '8', 'B2': '5', 'B3': '3', 'B8': '4', 'B9': '9', 'I9': '3', 'I8': '2',
                          'I1': '7', 'I3': '8', 'I2': '1', 'I5': '6', 'I4': '5', 'I7': '9', 'I6': '4', 'A1': '2',
                          'A3': '7', 'A2': '6', 'E9': '7', 'A4': '9', 'A7': '3', 'A6': '5', 'A9': '1', 'A8': '8',
                          'E7': '6', 'E6': '2', 'E1': '3', 'E3': '4', 'E2': '8', 'E8': '5', 'A5': '4', 'H8': '6',
                          'H9': '4', 'H2': '3', 'H3': '5', 'H1': '9', 'H6': '1', 'H7': '7', 'H4': '2', 'H5': '8',
                          'D8': '9', 'D9': '2', 'D6': '8', 'D7': '1', 'D4': '4', 'D5': '3', 'D2': '7', 'D3': '6',
                          'D1': '5'}
#print("\n")
#display(solved_diag_sudoku)