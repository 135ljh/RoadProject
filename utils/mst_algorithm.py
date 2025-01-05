# utils/mst_algorithm.py
from typing import List, Dict, Tuple
import heapq

class UnionFind:

    # 并查集的构造函数，接收一个整数 n，表示并查集中元素的数量。
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [1] * n

    # find 方法用于查找元素 p 所属的集合的根节点（即代表元）
    def find(self, p: int) -> int:
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
            # 路径压缩
            # 在查找过程中，将沿途的所有节点直接挂到根节点下，使得下次查找这些节点时可以直接到达根节点，从而加速后续的查找操作。
        return self.parent[p]

    # union 方法用于将两个元素 p 和 q 所属的集合合并为一个集合
    def union(self, p: int, q: int) -> None:
        # 分别找到 p 和 q 所属集合的根节点 rootP 和 rootQ
        rootP = self.find(p)
        rootQ = self.find(q)
        #如果 rootP 和 rootQ 相同，说明 p 和 q 已经属于同一个集合，无需进行任何操作，直接返回
        if rootP == rootQ:
            return

        # 按秩合并
        # 如果 rootP 的秩大于 rootQ 的秩，则将 rootQ 的父节点设置为 rootP，即把 rootQ 所在的树挂在 rootP 下。
        # 如果 rootP 的秩小于 rootQ 的秩，则将 rootP 的父节点设置为 rootQ，即把 rootP 所在的树挂在 rootQ 下。
        # 如果 rootP 和 rootQ 的秩相同，则任意选择一个作为新的根节点，并将该根节点的秩加 1，以保持树的平衡。
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
    # 排序边（按权重升序）
    roads.sort(key=lambda x: x['length'])
    # 创建了一个 UnionFind 对象，用于管理城镇之间的连通性
    uf = UnionFind(towns)
    # 遍历所有道路，构建最小生成树
    mst = []
    for road in roads:
        start = road['start'] - 1
        end = road['end'] - 1
        length = road['length']

        if uf.find(start) != uf.find(end):  #检查起点和终点是否属于同一个集合
            uf.union(start, end) #合并
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
    # 构建邻接表
    adj_list = {i: [] for i in range(1, towns + 1)} # 创建一个字典 adj_list，其中键是从 1 到 towns 的所有整数，每个键对应的值是一个空列表。
    for road in roads:
        start, end, length = road['start'], road['end'], road['length']
        adj_list[start].append((end, length))
        adj_list[end].append((start, length))

    # 初始化最小堆和辅助变量
    heap = [(0, 1, None)]  # (cost, current_node, prev_node) 分别表示边的权重、当前节点和前一个节点
    visited = set() # 用于记录已经访问过的城镇，避免重复处理
    mst = [] # 用于存储最小生成树中的边。

    #逐步构建最小生成树
    while heap and len(visited) < towns:
        # 从最小堆中弹出权重最小的边，获取当前节点 node、前一个节点 prev_node 和边的权重 cost。
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
# Kruskal 算法使用并查集来管理连通性，而 Prim 算法使用最小堆来选择权重最小的边。