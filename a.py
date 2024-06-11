# Hàm tính f(x, y)
def f(x, y):
    return -7955703807 + (x - 1) * (x // 2) - (y - 1) * (y // 2)

# Hàm tìm giá trị của x và y cho một giá trị z
def find_xy(z):
    # Khởi tạo giá trị ban đầu cho x và y
    x, y = 1, 1
    
    # Tính toán giá trị của f(x, y) cho giá trị ban đầu của x và y
    current_z = f(x, y)
    
    # Kiểm tra nếu giá trị ban đầu của f(x, y) là giá trị cần tìm
    if current_z == z:
        return x, y
    
    # Lặp qua các giá trị của x và y để tìm giá trị của f(x, y) bằng z
    while current_z < z:
        # Tăng giá trị của x và tính toán f(x, y)
        x += 1
        current_z = f(x, y)
        
        # Kiểm tra nếu f(x, y) bằng z
        if current_z == z:
            return x, y
        
        # Tăng giá trị của y và tính toán f(x, y)
        y += 1
        current_z = f(x, y)
        
        # Kiểm tra nếu f(x, y) bằng z
        if current_z == z:
            return x, y
    
    # Trả về None nếu không tìm thấy giải pháp
    return None

# Giá trị z
z = 1027959367612

# Tìm x và y
result = find_xy(z)

# In kết quả
if result:
    x, y = result
    print("x =", x, "y =", y)
else:
    print("Không tìm thấy giải pháp.")
