def find_coordinates(z, f_11):

    f = f_11
    x, y = 1, 1

    while f != z:
        if x < y:
            f += x
            x += 1
        else:
            f -= y
            y += 1

    return x, y

f_11 = 105546231015
z = 979069105696

x, y = find_coordinates(z, f_11)
print(f"{x},{y}")