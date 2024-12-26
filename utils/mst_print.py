# utils/mst_print.py

from typing import List, Dict
import collections


def dfs_print_tree(edges: List[Dict[str, int]], root: int, adj_list: Dict[int, List[int]], visited: set,
                   depth: int) -> None:
    """
    使用递归 DFS 打印最小生成树。

    :param edges: 最小生成树中的所有边
    :param root: 当前根节点
    :param adj_list: 邻接表
    :param visited: 已访问的节点集合
    :param depth: 当前深度
    """
    if root in visited:
        return
    visited.add(root)

    # 找到与当前节点相连的边
    connected_edges = [edge for edge in edges if edge['start'] == root or edge['end'] == root]

    # 打印当前节点及其相连的边
    print('  ' * depth + f'└── {root}')
    for edge in connected_edges:
        start, end = edge['start'], edge['end']
        if start == root and end not in visited:
            print('  ' * (depth + 1) + f'├── 边: {start} -> {end}, 长度: {edge["length"]}')
            dfs_print_tree(edges, end, adj_list, visited, depth + 2)
        elif end == root and start not in visited:
            print('  ' * (depth + 1) + f'├── 边: {end} -> {start}, 长度: {edge["length"]}')
            dfs_print_tree(edges, start, adj_list, visited, depth + 2)


def print_mst_tree_kruskal(kruskal_result: Dict[str, List[Dict[str, int]]]) -> None:
    """
    以树形结构打印 Kruskal 算法生成的最小生成树。

    :param kruskal_result: Kruskal 算法生成的最小生成树结果
    """
    mst = kruskal_result['newRoads']

    # 构建邻接表
    adj_list = {i: [] for i in range(1, len(mst) + 2)}  # 假设节点编号从 1 开始
    for road in mst:
        start, end = road['start'], road['end']
        adj_list[start].append(end)
        adj_list[end].append(start)

    # 选择任意一个节点作为根节点（这里选择 1 号节点）
    root = 1
    visited = set()

    print("Kruskal 最小生成树 (树形结构):")
    dfs_print_tree(mst, root, adj_list, visited, 0)


def print_mst_tree_prim(prim_result: Dict[str, List[Dict[str, int]]]) -> None:
    """
    以树形结构打印 Prim 算法生成的最小生成树。

    :param prim_result: Prim 算法生成的最小生成树结果
    """
    mst = prim_result['newRoads']

    # 构建邻接表
    adj_list = {i: [] for i in range(1, len(mst) + 2)}  # 假设节点编号从 1 开始
    for road in mst:
        start, end = road['start'], road['end']
        adj_list[start].append(end)
        adj_list[end].append(start)

    # 选择 1 号节点作为根节点（Prim 算法的起点）
    root = 1
    visited = set()

    print("Prim 最小生成树 (树形结构):")
    dfs_print_tree(mst, root, adj_list, visited, 0)