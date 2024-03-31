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
        mapping = ["course", "programme", "course_level", "breadth_req", "lecture"]
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

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def calculate_review_score(self, course: Any) -> int | float:
        """Calculate the average review score for a given course based on reviews from all users.
        """
        if course not in self._vertices or not isinstance(self._vertices[course], _Course):
            return 0
        course_vertex = self._vertices[course]
        if not course_vertex.review_scores:
            return 0
        total_score = sum(course_vertex.review_scores)
        all_review_type = len(course_vertex.review_scores)

        return total_score / all_review_type

    def calculate_pre_cor_score(self, course: Any, student_completed_courses: list[str]) -> int | float:
        """Calculate a score for a given course based on the alignment of its prerequisites with courses
         a student has completed and the presence of corequisites.
        """
        if course not in self._vertices or not isinstance(self._vertices[course], _Course):
            return 0
        course_vertex = self._vertices[course]
        input_course_lecture = course_vertex.get_neighbours(kind='lecture')
        pre_cor_score = 0
        input_course_pre_cor = set()

        for lecture_vertex in input_course_lecture:
            input_course_pre_cor.update(lecture_vertex.prerequisite)
            input_course_pre_cor.update(lecture_vertex.corequisite)

        relevant_input_pre_cor = input_course_pre_cor.intersection(set(student_completed_courses))

        for other_course_item, other_course_vertex in self._vertices.items():
            if other_course_vertex.kind == 'course' and other_course_item != course:
                other_lectures = other_course_vertex.get_neighbours(kind='lecture')
                other_pre_cor = set()
                for lecture_vertex in other_lectures:
                    other_pre_cor.update(lecture_vertex.prerequisite)
                    other_pre_cor.update(lecture_vertex.corequisite)
                    overlap = relevant_input_pre_cor.intersection(other_pre_cor)
                    if overlap:
                        pre_cor_score += len(overlap)
        return pre_cor_score

    def calculate_program_score(self, course: Any) -> int | float:
        """Calculate the program score for a given course based on its connections to program vertices.
        """
        if course not in self._vertices or not isinstance(self._vertices[course], _Course):
            return 0

        program_score = 0
        program_for_course = self._vertices[course].get_neighbours(kind='programme')

        for other_course_item, other_course_vertex in self._vertices.items():
            if other_course_vertex.kind == 'course' and other_course_item != course:
                other_course_program = other_course_vertex.get_neighbours(kind='programme')
                shared_program = program_for_course.intersection(other_course_program)
                if shared_program:
                    program_score += 1

        return program_score

    def calculate_breadth_score(self, course: Any) -> int | float:
        """Calculate the breadth score for a given course based on the alignment of breadth requirement
        numbers with other courses in the graph.
        """
        if course not in self._vertices or not isinstance(self._vertices[course], _Course):
            return 0

        breadth_score = 0
        breadth_reqs_for_course = self._vertices[course].get_neighbours(kind='breadth_req')

        for other_course_item, other_course_vertex in self._vertices.items():
            if other_course_vertex.kind == 'course' and other_course_item != course:
                other_course_breadth_reqs = other_course_vertex.get_neighbours(kind='breadth_req')
                shared_breadth = breadth_reqs_for_course.intersection(other_course_breadth_reqs)
                if shared_breadth:
                    breadth_score += 1

        return breadth_score

    def calculate_course_level_score(self, course: Any) -> int | float:
        """Calculate score based on course level alignment."""
        if course not in self._vertices or not isinstance(self._vertices[course], _Course):
            return 0
        course_level_vertices = [n for n in self._vertices[course].get_neighbours(kind='course_level')]
        if len(course_level_vertices) != 1:
            return 0
        input_level = course_level_vertices[0].item
        level_score = 0

        for other_course_item, other_course_vertex in self._vertices.items():
            if other_course_vertex.kind == 'course' and other_course_item != course:
                other_level_vertices = [n for n in other_course_vertex.get_neighbours(kind='course_level')]
                if len(other_level_vertices) != 1:
                    continue
                other_level = other_level_vertices[0].item
                if input_level == other_level or (input_level != 4 and input_level + 1 == other_level):
                    level_score += 1

        return level_score

    def compute_total_score(self, course: Any, student_completed_courses: list[str]) -> int | float:
        """Compute the total score for a given course, combining review, breadth, programme, and
        prerequisite/corequisite scores.
        """
        weight_review = 0.1
        weight_pre_cor = 0.3
        weight_program = 0.2
        weight_breadth = 0.2
        weight_level = 0.2

        review_score = self.calculate_review_score(course)
        pre_cor_score = self.calculate_pre_cor_score(course, student_completed_courses)
        program_score = self.calculate_program_score(course)
        breadth_score = self.calculate_breadth_score(course)
        level_score = self.calculate_course_level_score(course)

        total_score = (review_score * weight_review +
                       pre_cor_score * weight_pre_cor +
                       program_score * weight_program +
                       breadth_score * weight_breadth +
                       level_score * weight_level)

        return total_score

    def recommend_courses(self, input_courses: list[str], student_completed_courses: list[str]) -> dict[str, list[str]]:
        """Recommend three courses for each course the user has input, there will also be a focus on the program
        user input
        """
        recommendations = {}

        for course in input_courses:
            score = {}
            for other_courses in self.get_all_vertices('course'):
                if other_courses not in input_courses:
                    total_score = self.compute_total_score(other_courses, student_completed_courses)
                    score[other_courses] = total_score
            top_3_recommendations = sorted(score, key=score.get, reverse=True)[:3]
            recommendations[course] = top_3_recommendations

        return recommendations


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
        - self.kind in {'course', 'programme', 'breadth_req', 'course_level', 'lecture'}
    """
    item: Any
    kind: str
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'course', 'programme', 'breadth_req', 'course_level', 'lecture'}
        """
        self.review_scores = []
        self.item = item
        self.kind = kind
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def get_neighbours(self, kind="") -> dict[Any, Any] | set[Any]:
        """Return neighbours of kind specified

        Preconditions:
          - kind in {'course', 'programme', 'breadth_req', 'course_level', 'lecture', ''}
        """

        self.detail = ""

        if kind == "":
            return self.neighbours
        else:
            return {n for n in self.neighbours.values() if n.kind == kind}


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
                g.add_vertex(r2[2], "course")
                g.add_vertex(r2[0], "programme")
                g.add_vertex(r2[3], "lecture")
                g.add_vertex(int(r2[2][3:4]), "course_level")
                g.add_edge(r2[2], r2[0])
                g.add_edge(r2[2], r2[3])
                g.add_edge(r2[2], int(r2[2][3:4]))

                breadthreqs = courses_breadthreq_mapping[r2[2]]
                for breadthreq in breadthreqs:
                    g.add_vertex(breadthreq, "breadth_req")
                    g.add_edge(r2[2], breadthreq)

    return g

if __name__ == "__main__":
    g = load_graph("dataset/review_small.csv", "dataset/course.csv")
