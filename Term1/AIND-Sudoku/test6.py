vv = {'B5': '47', 'C2': '257', 'H3': '47', 'I9': '2467', 'G8': '1478', 'C4': '8', 'B8': '278', 'C1': '25', 'G1': '134', 'H1': '8', 'D4': '1', 'A3': '3', 'A6': '147', 'B2': '24678', 'I1': '46', 'D3': '8', 'G4': '6', 'D9': '34567', 'I6': '47', 'I8': '24678', 'A7': '6', 'E9': '8', 'G6': '9', 'H8': '1467', 'E1': '7', 'E5': '34569', 'C8': '23579', 'H6': '3', 'F7': '2', 'E4': '459', 'I2': '4679', 'G3': '2', 'F6': '8', 'D2': '345', 'I4': '4', 'D8': '34567', 'C7': '4', 'B3': '47', 'C3': '1', 'E6': '4', 'A4': '49', 'C5': '79', 'G5': '478', 'F3': '6', 'F9': '345', 'G9': '47', 'C6': '6', 'E8': '13456', 'H2': '1467', 'A5': '2', 'E3': '49', 'C9': '2357', 'H9': '9', 'B6': '5', 'B9': '1', 'F2': '13459', 'G2': '1347', 'I7': '3', 'I5': '1', 'E7': '1', 'A9': '57', 'A8': '5789', 'A1': '45', 'H7': '17', 'F5': '3459', 'H4': '2', 'B4': '3', 'G7': '5', 'D5': '3456', 'H5': '457', 'E2': '123459', 'D6': '2', 'B1': '9', 'F4': '7', 'F1': '1345', 'D7': '9', 'I3': '5', 'A2': '4578', 'F8': '1345', 'D1': '345', 'B7': '78'}
display(vv)

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
    
    values_c = values.copy()
    tab = {}
    for k, v in values_c.items():
    	if len(v) > 1:
    		change = False
    		for unit in units[k]:
    			strr = "".join([str(values_c[vu]) for vu in unit if len(values_c[vu]) > 1])
    			for nb in v:
    				if strr.count(str(nb)) == 1:
    					tab[k] = nb
    					change = True
    					break
    			if change:
    				change = False
    				break

    for k, v in tab.items():
    	values_c[k] = tab[k]
    	#print("change ", k, " by ", v)
    return values_c

print("\n")
rt = only_choice(vv)
print("\n")
display(rt)
rt1 = only_choice(vv)
print("\n")
display(rt1)
rt2 = only_choice(vv)
print("\n")
display(rt2)