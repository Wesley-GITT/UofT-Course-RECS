from __future__ import annotations
# import csv
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
        if item not in self._vertices:
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
        if course not in self._vertices:
            return 0

        course_vertex = self._vertices[course]
        total_score = 0
        num_of_review = 0

        for neighbour, weight in course_vertex.neighbours.items():
            if neighbour.kind == 'user':
                total_score += weight
                num_of_review += 1

        average_score = total_score / num_of_review if num_of_review != 0 else 0.0

        return average_score

    def calculate_breath_score(self, course: Any) -> int | float:
        """Calculate the breadth score for a given course based on the alignment of breadth requirement
        numbers with other courses in the graph.
        """
        if course not in self._vertices or not self._vertices[course].breath_num:
            return 0

        course_vertex = self._vertices[course]
        breath_requirement = set(course_vertex.breath_num)
        breath_score = 0

        for course_item, course_vertex in self._vertices.items():
            if course_vertex.kind == 'course' and course_item != course:
                shared_breath = breath_requirement.intersection(set(course_vertex.breath_num))
                if shared_breath:
                    breath_score += len(shared_breath)

        return breath_score

    def calculate_program_score(self, course: Any, program: str) -> int | float:
        """Calculate the program score for a given course based on its connections to program vertices.
        """
        if course not in self._vertices:
            return 0

        course_vertex = self._vertices[course]

        if any(neighbour.item == program for neighbour in course_vertex.neighbours if neighbour.kind == 'programme'):
            program_score = 1
        else:
            program_score = 0

        return program_score

    def calculate_pre_cor_score(self, course: Any, student_completed_courses: list[str]) -> int | float:
        """Calculate a score for a given course based on the alignment of its prerequisites with courses
         a student has completed and the presence of corequisites.
        """
        if course not in self._vertices:
            return 0
        course_vertex = self._vertices[course]
        pre_score = 0
        cor_score = 0

        if course_vertex.prerequisite:
            matched_pre = [pre for pre in course_vertex.prerequisite if pre in student_completed_courses]
            pre_score = len(matched_pre) / len(course_vertex.prerequisite) if course_vertex.prerequisite else 0

        if course_vertex.corequisite:
            cor_score = len(course_vertex.corequisite) / (len(course_vertex.corequisite) + 1)

        return (pre_score + cor_score) / 2

    def compute_total_score(self, course: Any, program: str, student_completed_courses: list[str]):
        """Compute the total score for a given course, combining review, breadth, programme, and
        prerequisite/corequisite scores.
        """
        weight_review = 0.3
        weight_breadth = 0.2
        weight_program = 0.3
        weight_pre_cor = 0.2

        review_score = self.calculate_review_score(course)
        breadth_score = self.calculate_breath_score(course)
        program_score = self.calculate_program_score(course, program)
        pre_cor_score = self.calculate_pre_cor_score(course, student_completed_courses)

        total_score = (review_score * weight_review +
                       breadth_score * weight_breadth +
                       program_score * weight_program +
                       pre_cor_score * weight_pre_cor)

        return total_score

    def recommend_courses(self, input_courses: list[str], input_program: str) -> dict[str, list[str]]:
        """Recommend three courses for each course the user has input, there will also be a focus on the program
        user input
        """
        recommendations = {}

        for course in input_courses:
            score = {}
            for other_courses in self.get_all_vertices('course'):
                if other_courses not in input_courses:
                    total_score = self.compute_total_score(other_courses, input_program, input_courses)
                    score[other_courses] = total_score
            top_3_recommendations = sorted(score, key=score.get, reverse=True)[:3]
            recommendations[course] = top_3_recommendations

        return recommendations


class _Vertex:
    """

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or course.
        - kind: The type of this vertex: 'user' or 'course'.
        - prerequisite: A list of string representing all prerequisite courses of this course
        - corequisite:  A list of string representing all corequisite courses of this course
        - breath_num: The breath_requirement number, in 12345
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'course', 'programme', 'breath'}
    """
    item: Any
    kind: str
    prerequisite: Optional[list[str]]
    corequisite: Optional[list[str]]
    breath_num: Optional[set[int]]
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any, kind: str, prerequisite: list[str], corequisite: list[str],
                 breath_num: set[int]) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = {}
        self.prerequisite = prerequisite
        self.corequisite = corequisite
        self.breath_num = breath_num

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)
