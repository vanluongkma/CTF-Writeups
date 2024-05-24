def find_final_nodes(n, edges, m, moves):
    from collections import defaultdict, deque
    
    def build_tree(n, edges):
        tree = defaultdict(list)
        for e1, e2 in edges:
            tree[e1].append(e2)
            tree[e2].append(e1)
        return tree
    
    def dfs(tree, start, end):
        stack = [(start, [start])]
        visited = set()
        while stack:
            node, path = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            if node == end:
                return path
            for neighbor in tree[node]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
        return []
    
    tree = build_tree(n, edges)
    results = []
    
    for s, d, e in moves:
        if s == d:
            results.append(s)
            continue
        path = dfs(tree, s, d)
        if len(path) <= e:
            results.append(d)
        else:
            results.append(path[e])
    
    return results

from pwn import*
from tqdm import*
io = remote("94.237.61.26", 59497)

def main():
    
    for _ in trange(100):
        io.recvuntil(b'/100\n')
        n = int(io.recvuntil(b'\n',drop=True).decode())
        edges = []
        for _ in range(n - 1):
            e1, e2 = map(int, io.recvuntil(b'\n',drop=True).decode().split())
            edges.append((e1, e2))
        
        m = int(io.recvuntil(b'\n',drop=True).decode())
        moves = []
        for _ in range(m):
            s, d, e = map(int, io.recvuntil(b'\n',drop=True).decode().split())
            moves.append((s, d, e))
        
        results = find_final_nodes(n, edges, m, moves)
        for result in results:
            io.sendline(str(result).encode())
    
    io.interactive()

if __name__ == "__main__":
    main()