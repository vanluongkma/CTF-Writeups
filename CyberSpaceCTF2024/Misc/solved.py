# from pwn import *

# f = connect("game-with-rin.challs.csc.tf", 1337, level = 'debug')
# f.recvuntil(b"    python3 <(curl -sSL https://goo.gle/kctf-pow) solve ")
# token = f.recvline()
# f.recvline()
# print(token)

# def solve_pow():
#     pow_command = "python3 <(curl -sSL https://goo.gle/kctf-pow) solve " + str(token)
#     pow_result = os.popen(pow_command).read().strip()
#     return pow_result

# print(solve_pow())

from pwn import *
import networkx as nx

# Connect to the game server
def connect_to_server():
    return connect("game-with-rin.challs.csc.tf", 1337, level='debug')

# Function to choose a spanning tree using NetworkX
def find_spanning_tree(V, edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    # Compute a Minimum Spanning Tree
    mst_edges = nx.minimum_spanning_tree(G).edges()
    return sorted([edges.index((u, v, w)) for u, v, w in mst_edges])

# Function to choose subset T (for the second player)
def choose_subset_T(S):
    # Example strategy: choose the first edge in the subset S
    return [S[0]]

# Main function to interact with the game
def main():
    f = connect_to_server()
    
    # Receive the PoW challenge token
    f.recvuntil(b"solve ")
    token = f.recvline().strip().decode()
    
    # Print the token and solve the PoW (assumed already solved and provided)
    print(f"PoW token: {token}")
    pow_result = input("Enter PoW result: ")
    f.sendline(pow_result.encode())
    
    # Start interacting with the game
    while True:
        # Receive game instructions
        f.recvuntil(b"Round ")
        round_number = int(f.recvline().strip().decode())
        f.recvuntil(b"V = ")
        V = int(f.recvline().strip().decode())
        f.recvuntil(b"edges = ")
        edges = eval(f.recvline().strip().decode())
        
        print(f"Round {round_number}, V = {V}")
        print(f"Edges: {edges}")

        # Decide whether to go first or second
        f.recvuntil(b"Do you want to go [first] or [second]?")
        response = "first"  # You can also choose "second" based on the strategy
        f.sendline(response.encode())

        if response == "first":
            # Choose subset S (spanning tree)
            S = find_spanning_tree(V, edges)
            S_str = " ".join(map(str, S))
            f.recvuntil(b"Please choose S")
            f.sendline(S_str.encode())
            f.recvuntil(b"Please choose T")
            # As the first player, you do not choose T
            continue
        else:
            # As the second player, you choose subset T
            S = list(map(int, input("Enter subset S: ").strip().split()))
            T = choose_subset_T(S)
            T_str = " ".join(map(str, T))
            f.sendline(T_str.encode())
            continue

        # Receive the result of the round and print it
        result = f.recvline().decode().strip()
        print(result)
        
        if "flag" in result:
            break

if __name__ == "__main__":
    main()
