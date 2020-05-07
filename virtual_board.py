def find_fields():
    #Pierwsze pole planszy
    start_x = 5
    start_y = 5

    #Kolejne pola
    next = 75

    fields_pos = []

    for j in range(0, 8):
        for i in range(0, 8):
            fields_pos.append([[start_x, start_y], [start_x + next, start_y + next]])
            start_x += next
        start_x = 5
        start_y += next

    return fields_pos

def move(checkers_list_before, checkers_list_after):
    positions = []

    for i in range(len(checkers_list_before)):
        if checkers_list_before[i] != checkers_list_after[i]:
            positions.append(i)

    if len(positions) == 2:
        if (checkers_list_after[positions[1]] == 'RP' and checkers_list_before[positions[1]] == None):
            print('CZERWONY')
            if (positions[1] == positions[0] + 7 or positions[1] == positions[0] + 9):
                return True
            else:
                return False
        elif (checkers_list_after[positions[0]] == 'WP' and checkers_list_before[positions[0]] == None):
            print('BIAŁY')
            if (positions[0] == positions[1] - 7 or positions[0] == positions[1] - 9):
                return True
            else:
                return False
        elif (checkers_list_after[positions[1]] == 'RQ' and checkers_list_before[positions[1]] == None):
            print('CZERWONA DAMA')
            if (positions[1] == positions[0] + 7 or positions[1] == positions[0] + 9 or positions[1] == positions[0] + 14 or
                positions[1] == positions[0] + 18 or positions[1] == positions[0] + 21 or positions[1] == positions[0] + 27 or
                positions[1] == positions[0] + 28 or positions[1] == positions[0] + 36 or positions[1] == positions[0] + 35 or
                positions[1] == positions[0] + 45 or positions[1] == positions[0] + 42 or positions[1] == positions[0] + 54 or
                positions[1] == positions[0] + 49 or positions[1] == positions[0] + 63):

                if((positions[1] - positions[0]) % 7 == 0):
                    for i in range(positions[0] + 7, positions[1], 7):
                        if checkers_list_before[i] != None:
                            return False

                elif ((positions[1] - positions[0]) % 9 == 0):
                    for i in range(positions[0] + 9, positions[1], 9):
                        if checkers_list_before[i] != None:
                            return False

                return True

            else:
                return False
        elif (checkers_list_after[positions[0]] == 'RQ' and checkers_list_before[positions[0]] == None):
            print('CZERWONA DAMA')
            if (positions[0] == positions[1] - 7 or positions[0] == positions[1] - 9 or positions[0] == positions[1] - 14 or
                positions[0] == positions[1] - 18 or positions[0] == positions[1] - 21 or positions[0] == positions[1] - 27 or
                positions[0] == positions[1] - 28 or positions[0] == positions[1] - 36 or positions[0] == positions[1] - 35 or
                positions[0] == positions[1] - 45 or positions[0] == positions[1] - 42 or positions[0] == positions[1] - 54 or
                positions[0] == positions[1] - 49 or positions[0] == positions[1] - 63):

                if ((positions[0] - positions[1]) % 7 == 0):
                    print(positions[0], positions[1])
                    for i in range(positions[0], positions[1], 7):
                        if checkers_list_before[i] != None:
                            return False

                elif ((positions[0] - positions[1]) % 9 == 0):
                    for i in range(positions[0], positions[1], 9):
                        if checkers_list_before[i] != None:
                            return False

                return True
            else:
                return False
        elif (checkers_list_after[positions[1]] == 'WQ' and checkers_list_before[positions[1]] == None):
            print('BIAŁA DAMA')
            if (positions[1] == positions[0] + 7 or positions[1] == positions[0] + 9 or positions[1] == positions[0] + 14 or
                positions[1] == positions[0] + 18 or positions[1] == positions[0] + 21 or positions[1] == positions[0] + 27 or
                positions[1] == positions[0] + 28 or positions[1] == positions[0] + 36 or positions[1] == positions[0] + 35 or
                positions[1] == positions[0] + 45 or positions[1] == positions[0] + 42 or positions[1] == positions[0] + 54 or
                positions[1] == positions[0] + 49 or positions[1] == positions[0] + 63):

                if ((positions[1] - positions[0]) % 7 == 0):
                    for i in range(positions[0] + 7, positions[1], 7):
                        if checkers_list_before[i] != None:
                            return False

                elif ((positions[1] - positions[0]) % 9 == 0):
                    for i in range(positions[0] + 9, positions[1], 9):
                        if checkers_list_before[i] != None:
                            return False

                return True

            else:
                return False
        elif(checkers_list_after[positions[0]] == 'WQ' and checkers_list_before[positions[0]] == None):
            print('BIAŁA DAMA')
            if (positions[0] == positions[1] - 7 or positions[0] == positions[1] - 9 or positions[0] == positions[1] - 14 or
                positions[0] == positions[1] - 18 or positions[0] == positions[1] - 21 or positions[0] == positions[1] - 27 or
                positions[0] == positions[1] - 28 or positions[0] == positions[1] - 36 or positions[0] == positions[1] - 35 or
                positions[0] == positions[1] - 45 or positions[0] == positions[1] - 42 or positions[0] == positions[1] - 54 or
                positions[0] == positions[1] - 49 or positions[0] == positions[1] - 63):
                if ((positions[0] - positions[1]) % 7 == 0):
                    print(positions[0], positions[1])
                    for i in range(positions[0], positions[1], 7):
                        if checkers_list_before[i] != None:
                            return False

                elif ((positions[0] - positions[1]) % 9 == 0):
                    for i in range(positions[0], positions[1], 9):
                        if checkers_list_before[i] != None:
                            return False

                return True
            else:
                return False

        else:
            return
