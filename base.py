from __future__ import annotations
import csv
from typing import Any, Union, Optional


# import networkx as nx


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

    def get_all_vertices(self, kind: str = '') -> set[_Vertex]:
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

        v1 = self._vertices[item1]
        v2 = self._vertices[item2]
        return v1.get_similarity_score(v2)

    def get_course_similarity(self, course: str) -> dict[str, float]:
        """Return a dictionary of course with their similarity score"""

        mapping = {}
        all_courses = self.get_all_vertices("course")
        for _course in all_courses:
            if _course != course:
                new_score = self.similarity_score(course, _course)
                mapping[_course] = new_score

        return mapping

    def recommend_courses(self, courses: list[str], filter_programme: str = "", limit: int = 3) -> list[str]:
        """Return a list of up to <limit> recommended courses based on similarity to the list of courses.

        Preconditions:
            - All({course in self._vertices for course in courses})
            - All({self._vertices[course].kind == 'course' for course in courses})
            - (filter_programme in self._vertices and self._vertices[filter_programme].kind == "programme") or filter_programme == ""
            - limit >= 1
        """

        recommended_course = []
        course_score = {}
        for course in courses:
            course_score_mapping = self.get_course_similarity(course)
            for _course in course_score_mapping:
                if _course not in courses:
                    if _course not in course_score:
                        course_score[_course] = 0.0
                    course_score[_course] += course_score_mapping[_course]

        for new_crs in course_score:
            if (new_crs[0:3] == filter_programme or filter_programme == "") and course_score[new_crs] != 0.0:
                next_index = 0
                for crs in recommended_course:
                    new_crs_score = course_score[new_crs]
                    crs_score = course_score[crs]

                    if new_crs_score < crs_score or (new_crs_score == crs_score and new_crs > crs):
                        next_index += 1

                recommended_course.insert(next_index, new_crs)

        return recommended_course[:limit]


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
        self.review_scores = []
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

    def get_similarity_score(self, other: _Vertex) -> float:
        """Return the weighted similarity score between this vertex and other.

        Raise a ValueError if the two vertices are of different kind
        """

        if len(self.neighbours) == 0 or len(other.neighbours) == 0:
            return 0.0
        else:
            numerator = 0.0
            v_union = set()
            for v1 in self.neighbours:
                v_union.add(v1)

                for v2 in other.neighbours:
                    if v1.item == v2.item and self.__weighted_helper(v1) == other.__weighted_helper(v2):
                        numerator += 1.0

                    if v2 not in v_union:
                        v_union.add(v2)

            return numerator / len(v_union)

def review_score_sum(row: list) -> float:
    """Helper function of load_graph. Return a sum of review scores."""
    sum = 0
    for score in row[8:17]:
        if score != "N/A":
            sum += float(score)

    return sum / 40


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

    courses_breadthreq_mapping = {}

    with open(course_file, 'r') as f:
        reader = csv.reader(f, delimiter="|")

        for r1 in reader:
            lst = []
            breadthreqs = r1[4].split(",")
            for breadthreq in breadthreqs:
                breadthreq = breadthreq.strip().lower()
                if breadthreq in breadthreq_mapping:
                    lst.append(breadthreq_mapping[breadthreq])
            courses_breadthreq_mapping[r1[0]] = lst

    with open(reviews_file, 'r') as f:
        reader = csv.reader(f, delimiter=":")

        for r2 in reader:
            if r2[2] in courses_breadthreq_mapping:
                course = r2[2]
                course_level = int(r2[2][3:4])
                professor = r2[4] + " " + r2[5]
                programme = r2[2][0:3]
                g.add_vertex(course, "course")
                g.add_vertex(programme, "programme")
                g.add_vertex(professor, "professor")
                g.add_vertex(course_level, "course_level")
                g.add_edge(course, programme)
                g.add_edge(course, professor, review_score_sum(r2))
                g.add_edge(course, course_level)

                breadthreqs = courses_breadthreq_mapping[r2[2]]
                for breadthreq in breadthreqs:
                    g.add_vertex(breadthreq, "breadth_req")
                    g.add_edge(r2[2], breadthreq)

    return g

if __name__ == "__main__":
    g = load_graph("dataset/review_full.csv", "dataset/course.csv")
    recs = g.recommend_courses(["MAT223H1"], limit=10)
    print(recs)
