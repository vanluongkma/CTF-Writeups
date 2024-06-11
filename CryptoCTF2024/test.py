def calculate_f(x, y):
    initial_value = 883376001270
    f_value = initial_value
    
    # Tính f(x, 1)
    for i in range(2, x + 1):
        f_value += (i - 1)
    
    # Tính f(x, y)
    for j in range(2, y + 1):
        f_value -= (j - 1)
    
    return f_value

def find_xy(target_z):
    for x in range(1, 1000000):  # Giới hạn tìm kiếm x và y
        for y in range(1, 1000000):
            if calculate_f(x, y) == target_z:
                return x, y
            if calculate_f(x, y) < target_z:
                break  # Bỏ qua các giá trị y tiếp theo nếu giá trị nhỏ hơn target_z
    
    return None, None

z = 1863552337043
x, y = find_xy(z)
print(f"x = {x}, y = {y}")
