import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

_GOAL_POS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan (admissível e consistente), ignorando o vazio."""
        total = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            r, c = divmod(i, 3)
            gr, gc = _GOAL_POS[tile]
            total += abs(r - gr) + abs(c - gc)
        return total

    def search(self, initial: State) -> SearchResult:
        tie = count()  # desempate estável no heap
        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_g = {initial: initial.cost}
        expanded = 0
        generated = 1
        max_frontier = 1

        while frontier:
            _, _, node = heapq.heappop(frontier)
            if node.cost > best_g.get(node, float("inf")):
                continue  # entrada obsoleta
            if node.is_goal:
                return SearchResult(node, expanded, generated, max_frontier, node.cost)
            expanded += 1
            for child in node.neighbors():
                if child.cost >= best_g.get(child, float("inf")):
                    continue
                best_g[child] = child.cost
                generated += 1
                heapq.heappush(frontier, (child.cost + self.heuristic(child), next(tie), child))
            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, expanded, generated, max_frontier, 0)
