from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        generated = 1
        expanded = 0
        if initial.is_goal:
            return SearchResult(initial, expanded, generated, 1, initial.cost)

        frontier = deque([initial])
        visited = {initial}
        max_frontier = 1

        while frontier:
            node = frontier.popleft()
            expanded += 1
            for child in node.neighbors():
                if child in visited:
                    continue
                generated += 1
                if child.is_goal:  # teste de objetivo na geração (ótimo na BFS)
                    return SearchResult(child, expanded, generated,
                                        max(max_frontier, len(frontier) + 1), child.cost)
                visited.add(child)
                frontier.append(child)
            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, expanded, generated, max_frontier, 0)
