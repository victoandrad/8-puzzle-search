from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        """DFS com limite de profundidade. Evita ciclos no caminho atual e
        reabre estados alcançados por um caminho mais curto."""
        frontier = [initial]  # pilha
        best_depth = {initial: initial.cost}
        expanded = 0
        generated = 1
        max_frontier = 1

        while frontier:
            node = frontier.pop()
            if node.is_goal:
                return SearchResult(node, expanded, generated, max_frontier, node.cost)
            if node.cost >= self.depth_limit:
                continue
            expanded += 1
            # inverte para explorar os filhos na ordem de neighbors()
            for child in reversed(node.neighbors()):
                if child.cost >= best_depth.get(child, float("inf")):
                    continue
                best_depth[child] = child.cost
                generated += 1
                frontier.append(child)
            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, expanded, generated, max_frontier, 0)
