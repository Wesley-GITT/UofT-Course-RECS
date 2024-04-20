"""Python file that contains graph and vertex class"""

from __future__ import annotations
from typing import Any, Union
import csv
import networkx as nx


class Graph:
    """A weighted graph used to represent a book review network that keeps track of review scores.

    Note that this is a subclass of the Graph class from Exercise 3, and so inherits any methods
    from that class that aren't overridden here.
    """
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.
        """
        mapping = ["course", "programme", "course_level", "breadth_req", "professor"]
        if item not in self._vertices and kind in mapping:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float] = 1) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.
        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.
        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set[str]:
        """Return a set of all vertex items in this graph.
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def similarity_score(self, item1: str, item2: str) -> float:
        """Get similarity score

        Raise ValueError if one of the item is not in the graph
        """

        if item1 not in self._vertices or item2 not in self._vertices:
            raise ValueError

        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.get_similarity_score(v2)

    def recommend_courses(self, courses: list[str], limit: int = 3) -> dict[str, list[str]]:
        """Return a list of up to <limit> recommended courses based on similarity to the list of courses.

        Preconditions:
            - All({course in self._vertices for course in courses})
            - All({self._vertices[course].kind == 'course' for course in courses})
            - limit >= 1
        """

        recommended_course = {}
        for course in courses:
            sub_recommended_course = []
            sub_recommended_course_mapping = {}
            for new_crs in self.get_all_vertices("course"):
                if new_crs in course:
                    continue

                next_index = 0
                new_crs_score = self.similarity_score(course, new_crs)
                for crs in sub_recommended_course:
                    crs_score = sub_recommended_course_mapping[crs]

                    if new_crs_score < crs_score or (new_crs_score == crs_score and new_crs > crs):
                        next_index += 1

                sub_recommended_course_mapping[new_crs] = new_crs_score
                sub_recommended_course.insert(next_index, new_crs)

            recommended_course[course] = sub_recommended_course[:limit]

        return recommended_course

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.kind)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.kind)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


class _Vertex:
    """

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or course.
        - kind: The type of this vertex: 'course', 'programme', 'breath', 'course_level'.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'course', 'programme', 'breadth_req', 'course_level', 'professor'}
    """
    item: Any
    kind: str
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'course', 'programme', 'breadth_req', 'course_level', 'professor'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def __weighted_helper(self, other: _Vertex) -> float:
        """Return the weight between two vertex.
        """

        if other in self.neighbours:
            return self.neighbours[other]
        else:
            return 0.0

    def _similarity_score_helper(self, v1: _Vertex, other: _Vertex, v_n_and_u: list[set[_Vertex]], kind: str) -> None:
        """Helper function of get similarity score"""
        neighbours_set2 = set(n for n in other.neighbours if n.kind == kind)
        v_n = v_n_and_u[0]
        v_u = v_n_and_u[1]
        for v2 in neighbours_set2:
            if v1.item == v2.item and self.__weighted_helper(v1) == other.__weighted_helper(v2):
                v_n.add(v1)

            if v2 not in v_u:
                v_u.add(v2)

    def get_similarity_score(self, other: _Vertex) -> float:
        """Return the weighted similarity score between this vertex and other.

        Raise a ValueError if the two vertices are of different kind
        """

        if len(self.neighbours) == 0 or len(other.neighbours) == 0:
            return 0.0
        else:
            weight = {"programme": 0.4, "professor": 0.2, "breadth_req": 0.2, "course_level": 0.2}
            for kind in weight:
                v_n = set()
                v_u = set()
                neighbours_set1 = set(n for n in self.neighbours if n.kind == kind)
                for v1 in neighbours_set1:
                    v_u.add(v1)
                    self._similarity_score_helper(v1, other, [v_n, v_u], kind)

                if len(v_u) != 0:
                    weight[kind] *= len(v_n) / len(v_u)
                else:
                    weight[kind] = 0

            return sum(list(weight.values()))


def review_score_sum(row: list) -> float:
    """Helper function of load_graph. Return a sum of review scores."""
    sum_of_score = 0
    for score in row[8:17]:
        if score != "N/A":
            sum_of_score += float(score)

    return sum_of_score / 40


def load_graph(reviews_file: str, course_file: str) -> Graph:
    """Return a course review graph corresponding to the given datasets.

    Preconditions:
        - reviews_file is the path to a CSV file corresponding to the book review data
          format described on the assignment handout
        - course_file is the path to a CSV file corresponding to the book data
          format described on the assignment handout

    """

    g = Graph()
    breadthreq_mapping = {"creative and cultural representations (1)": 1,
                          "thought, belief, and behaviour (2)": 2,
                          "society and its institutions (3)": 3,
                          "living things and their environment (4)": 4,
                          "the physical and mathematical universes (5)": 5}

    course_level_mapping = {
        1: {"100": 10, "100/200": 15},
        2: {"200": 20, "100/200": 15, "200/300": 25},
        3: {"300": 30, "200/300": 25, "300/400": 35},
        4: {"400": 40, "300/400": 35}
    }

    courses_breadthreq_mapping = {}

    with open(course_file, 'r') as f:
        reader = csv.reader(f, delimiter="|")

        for row in reader:
            lst = []
            for breadthreq in row[4].split(","):
                if breadthreq in breadthreq_mapping:
                    lst.append(breadthreq_mapping[breadthreq.strip().lower()])
            courses_breadthreq_mapping[row[0]] = lst

    with open(reviews_file, 'r') as f:
        reader = csv.reader(f, delimiter=":")

        for row in reader:
            if row[2] in courses_breadthreq_mapping:
                mapping = {
                    "course": row[2],
                    "course_level": int(row[2][3:4]),
                    "professor": row[4] + " " + row[5],
                    "programme": row[2][0:3]
                }
                g.add_vertex(mapping["course"], "course")
                g.add_vertex(mapping["programme"], "programme")
                g.add_vertex(mapping["professor"], "professor")
                g.add_edge(mapping["course"], mapping["programme"])
                g.add_edge(mapping["course"], mapping["professor"], review_score_sum(row))

                course_levels = course_level_mapping[mapping["course_level"]]
                for crs_level_key in course_levels:
                    g.add_vertex(crs_level_key, "course_level")
                    g.add_edge(mapping["course"], crs_level_key, course_levels[crs_level_key])

                breadthreqs = courses_breadthreq_mapping[mapping["course"]]
                for breadthreq in breadthreqs:
                    g.add_vertex(breadthreq, "breadth_req")
                    g.add_edge(mapping["course"], breadthreq)

    return g


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv'],
        'allowed-io': ['load_graph']
    })
