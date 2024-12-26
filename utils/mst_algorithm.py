# utils/mst_algorithm.py
from typing import List, Dict, Tuple
import heapq

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, p: int) -> int:
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])  # 路径压缩
        return self.parent[p]

    def union(self, p: int, q: int) -> None:
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP == rootQ:
            return

        # 按秩合并
        if self.rank[rootP] > self.rank[rootQ]:
            self.parent[rootQ] = rootP
        elif self.rank[rootP] < self.rank[rootQ]:
            self.parent[rootP] = rootQ
        else:
            self.parent[rootQ] = rootP
            self.rank[rootP] += 1

def calculate_mst_kruskal(towns: int, roads: List[Dict[str, int]]) -> Dict[str, List[Dict[str, int]]]:
    """
    使用破圈法 (Kruskal 算法) 计算最小生成树。
    """
    roads.sort(key=lambda x: x['length'])
    uf = UnionFind(towns)
    mst = []

    for road in roads:
        start = road['start'] - 1
        end = road['end'] - 1
        length = road['length']

        if uf.find(start) != uf.find(end):
            uf.union(start, end)
            mst.append({
                'start': start + 1,
                'end': end + 1,
                'length': length
            })

    if len(mst) < towns - 1:
        raise ValueError("无法形成完整的最小生成树，可能存在不连通的城镇")

    return {'newRoads': mst}

def calculate_mst_prim(towns: int, roads: List[Dict[str, int]]) -> Dict[str, List[Dict[str, int]]]:
    """
    使用避圈法 (Prim 算法) 计算最小生成树。
    """
    adj_list = {i: [] for i in range(1, towns + 1)}
    for road in roads:
        start, end, length = road['start'], road['end'], road['length']
        adj_list[start].append((end, length))
        adj_list[end].append((start, length))

    heap = [(0, 1, None)]  # (cost, current_node, prev_node)
    visited = set()
    mst = []

    while heap and len(visited) < towns:
        cost, node, prev_node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)

        if prev_node is not None:
            mst.append({
                'start': prev_node,
                'end': node,
                'length': cost
            })

        for neighbor, edge_cost in adj_list[node]:
            if neighbor not in visited:
                heapq.heappush(heap, (edge_cost, neighbor, node))

    if len(mst) < towns - 1:
        raise ValueError("无法形成完整的最小生成树，可能存在不连通的城镇")

    return {'newRoads': mst}

#这段代码实现了最小生成树的两种经典算法：Kruskal 和 Prim。
# Kruskal 算法使用并查集来管理连通性，而 Prim 算法使用优先队列来选择最小代价的边。