def min_cost(n, k, a):
    from collections import defaultdict
    import sys
    
    inf = sys.maxsize
    
    # Helper function to precompute costs
    def precompute_costs():
        cost = [[0] * n for _ in range(n)]
        for i in range(n):
            freq = defaultdict(int)
            pairs = 0
            for j in range(i, n):
                pairs += freq[a[j]]
                freq[a[j]] += 1
                cost[i][j] = pairs
        return cost
    
    # Precompute the costs for all subsegments
    cost = precompute_costs()
    
    # Initialize DP table
    dp = [[inf] * (k+1) for _ in range(n+1)]
    dp[0][0] = 0
    
    # Fill the DP table
    for segments in range(1, k+1):
        for end in range(1, n+1):
            for start in range(segments-1, end):
                dp[end][segments] = min(dp[end][segments], dp[start][segments-1] + cost[start][end-1])
    
    return dp[n][k]


# def min_cost(n, k, a):
#     from collections import defaultdict
    
#     # Function to calculate the cost of subsegment [i, j]
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

#     # Function to compute DP using divide and conquer optimization
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

#     # Compute DP for each partition count
#     for j in range(1, k + 1):
#         compute_dp(j, 1, n, 0, n)

#     return dp[n][k]

from pwn import*
from tqdm import*

io = remote("83.136.248.205", 43648)

def main():
    for _ in trange(100):
        io.recvuntil(b'/100\n')
        n, k = map(int, io.recvuntil(b'\n',drop=True).decode().split())
        array = list(map(int, io.recvuntil(b'\n',drop=True).decode().split()))

        # Gọi hàm tính toán và in ra kết quả
        result = min_cost(n, k, array)
        io.sendline(str(result).encode())
    io.interactive()
if __name__ == "__main__":
    main()