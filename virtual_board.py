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