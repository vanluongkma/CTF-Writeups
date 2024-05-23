# def min_cost(n, k, a):
#     from collections import defaultdict

#     # Tính chi phí của đoạn con [i, j]
#     def calculate_cost(start, end):
#         freq = defaultdict(int)
#         cost = 0
#         for i in range(start, end + 1):
#             if freq[a[i]] > 0:
#                 cost += freq[a[i]]
#             freq[a[i]] += 1
#         return cost

#     # Tiền tính toán chi phí cho tất cả các đoạn con
#     cost = [[0] * n for _ in range(n)]
#     for i in range(n):
#         freq = defaultdict(int)
#         current_cost = 0
#         for j in range(i, n):
#             if freq[a[j]] > 0:
#                 current_cost += freq[a[j]]
#             freq[a[j]] += 1
#             cost[i][j] = current_cost

#     # Khởi tạo mảng DP
#     dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
#     dp[0][0] = 0

#     # Hàm tính toán DP sử dụng phân chia và chinh phục
#     def compute_dp(j, l, r, opt_l, opt_r):
#         if l > r:
#             return
#         mid = (l + r) // 2
#         best_cost = float('inf')
#         best_pos = -1
#         for i in range(opt_l, min(mid, opt_r) + 1):
#             current_cost = dp[i][j - 1] + (cost[i][mid - 1] if i < mid else 0)
#             if current_cost < best_cost:
#                 best_cost = current_cost
#                 best_pos = i
#         dp[mid][j] = best_cost
#         compute_dp(j, l, mid - 1, opt_l, best_pos)
#         compute_dp(j, mid + 1, r, best_pos, opt_r)

#     # Tính toán DP cho mỗi số lượng phân đoạn
#     for j in range(1, k + 1):
#         compute_dp(j, 1, n, 0, n)

#     return dp[n][k]

# # Kết nối tới máy chủ từ xa
# from pwn import *
# from tqdm import *

# io = remote("83.136.248.205", 43648)

# def main():
#     for _ in trange(100):
#         io.recvuntil(b'/100\n')
#         n, k = map(int, io.recvuntil(b'\n', drop=True).decode().split())
#         array = list(map(int, io.recvuntil(b'\n', drop=True).decode().split()))

#         # Gọi hàm tính toán và gửi kết quả về máy chủ
#         result = min_cost(n, k, array)
#         io.sendline(str(result).encode())
#     io.interactive()

# if __name__ == "__main__":
#     main()


# def min_cost(n, k, a):
#     from collections import defaultdict
    
#     # Calculate the cost for subsegment [start, end]
#     def calculate_cost(start, end):
#         freq = defaultdict(int)
#         cost = 0
#         for i in range(start, end + 1):
#             if freq[a[i]] > 0:
#                 cost += freq[a[i]]
#             freq[a[i]] += 1
#         return cost
    
#     # Precompute the cost for all subsegments
#     cost = [[0] * n for _ in range(n)]
#     for i in range(n):
#         freq = defaultdict(int)
#         current_cost = 0
#         for j in range(i, n):
#             if freq[a[j]] > 0:
#                 current_cost += freq[a[j]]
#             freq[a[j]] += 1
#             cost[i][j] = current_cost

#     # Initialize DP array
#     dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
#     dp[0][0] = 0

#     def compute_dp(j, l, r, opt_l, opt_r):
#         if l > r:
#             return
#         mid = (l + r) // 2
#         best_cost = float('inf')
#         best_pos = -1
#         for i in range(opt_l, min(mid, opt_r) + 1):
#             current_cost = dp[i][j - 1] + (cost[i][mid - 1] if i < mid else 0)
#             if current_cost < best_cost:
#                 best_cost = current_cost
#                 best_pos = i
#         dp[mid][j] = best_cost
#         compute_dp(j, l, mid - 1, opt_l, best_pos)
#         compute_dp(j, mid + 1, r, best_pos, opt_r)

#     for j in range(1, k + 1):
#         compute_dp(j, 1, n, 0, n)

#     return dp[n][k]

# # Example usage with networking code
# if __name__ == "__main__":
#     from pwn import *
#     from tqdm import *

#     io = remote("83.136.248.205", 43648)

#     def main():
#         for _ in trange(100):
#             io.recvuntil(b'/100\n')
#             n, k = map(int, io.recvuntil(b'\n', drop=True).decode().split())
#             array = list(map(int, io.recvuntil(b'\n', drop=True).decode().split()))

#             # Gọi hàm tính toán và in ra kết quả
#             result = min_cost(n, k, array)
#             io.sendline(str(result).encode())

#     main()


def min_cost(n, k, a):
    from collections import defaultdict
    import sys
    sys.setrecursionlimit(200000)
    
    # Initialize DP array
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    # Function to add an element to the current segment
    def add(x):
        nonlocal current_cost
        if freq[a[x]] > 0:
            current_cost += freq[a[x]]
        freq[a[x]] += 1

    # Function to remove an element from the current segment
    def remove(x):
        nonlocal current_cost
        freq[a[x]] -= 1
        if freq[a[x]] > 0:
            current_cost -= freq[a[x]]

    # Function to calculate the cost of the segment [l, r]
    def cost(l, r):
        nonlocal cur_l, cur_r, current_cost
        while cur_r < r:
            cur_r += 1
            add(cur_r)
        while cur_r > r:
            remove(cur_r)
            cur_r -= 1
        while cur_l < l:
            remove(cur_l)
            cur_l += 1
        while cur_l > l:
            cur_l -= 1
            add(cur_l)
        return current_cost

    # Function to compute DP using divide and conquer optimization
    def compute_dp(j, l, r, opt_l, opt_r):
        if l > r:
            return
        mid = (l + r) // 2
        best_cost = float('inf')
        best_pos = -1

        for i in range(opt_l, min(mid, opt_r) + 1):
            current_cost = dp[i][j - 1] + cost(i, mid - 1)
            if current_cost < best_cost:
                best_cost = current_cost
                best_pos = i

        dp[mid][j] = best_cost
        compute_dp(j, l, mid - 1, opt_l, best_pos)
        compute_dp(j, mid + 1, r, best_pos, opt_r)

    cur_l, cur_r = 0, -1
    current_cost = 0
    freq = defaultdict(int)
    
    for j in range(1, k + 1):
        compute_dp(j, 1, n, 0, n - 1)

    return dp[n][k]

# Example usage with networking code
if __name__ == "__main__":
    from pwn import *
    from tqdm import *

    io = remote("83.136.248.205", 43648)

        for _ in trange(100):
            io.recvuntil(b'/100\n')
            n, k = map(int, io.recvuntil(b'\n', drop=True).decode().split())
            array = list(map(int, io.recvuntil(b'\n', drop=True).decode().split()))

            # Gọi hàm tính toán và in ra kết quả
            result = min_cost(n, k, array)
            io.sendline(str(result).encode())
        io.interactive()

    main()