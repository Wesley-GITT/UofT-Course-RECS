"""
Wrapping up
"""

import base
# Note: You may add helper functions, classes, etc. here as needed

def __input_similar_helper(item: str, set_to_find: set[str], limit: int = 5) -> str:
    """Helper function. Print if the input item is similar to one another."""
    threshold_score = 0.8
    similar_lst = []
    similar_score = {}
    for _item in set_to_find:
        item_score = 0.0
        for i in range(len(item)):
            for j in range(len(_item)):
                if i == j and item[i] == _item[j]:
                    item_score += 2.0 / (len(item) + len(_item))
                elif item[i] == _item[j]:
                    item_score += 0.01 / (len(item) + len(_item))

        if item_score >= threshold_score:
            next_index = 0
            for itm in similar_lst:
                if item_score < similar_score[itm] or (item_score == similar_score[itm] and _item > itm):
                    next_index += 1

            similar_lst.insert(next_index, _item)
            similar_score[_item] = item_score

    return str.join(", ", similar_lst[:limit])


def __input_helper(graph: base.Graph, input_kind: str, completed_str: str = "DONE") -> list[str]:
    """Helper function. Return a list of input courses or programme"""
    mset = set()
    choice = ""
    input_kind = str.join(" ", input_kind.split("_"))
    print()
    while choice.upper() != completed_str:
        choice = input(f"Enter {input_kind}: ").upper()
        set_to_find = graph.get_all_vertices(input_kind)
        if choice in set_to_find:
            if choice not in mset:
                mset.add(choice)
            else:
                print(f"You have already entered this {input_kind}.")
        elif choice.upper() != completed_str:
            similar_str = __input_similar_helper(choice, set_to_find)
            if similar_str != "":
                print(f"Did you mean one of the following?\n{similar_str}\n")
            else:
                print(f"{choice} is not a/an {input_kind} in our dataset.\n")

    print(f"Your input on {input_kind}: {list(mset)}")
    return list(mset)


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    g = base.load_graph("dataset/review_full.csv", "dataset/course.csv")
    print("Welcome to the Course Recommendation Service(UofT version)")
    name = input("Please enter your name to continue: ")
    print("Hi, " + name + ". You can now enter the courses you have completed or is taking this year\n")
    print("Enter one course you have taken or is taking.")
    courses = __input_helper(g, "course")

    recommendation = g.recommend_courses(courses, 3)

    print("\nThe recommendation course we would like to provides to you is follows")
    print("We have recommend three courses for the each course you entered")
    print(recommendation)

    print("\nFor further information on pre-requisite courses and co-requisite course.")
    print("please view the following websites we provided")

    website = f"https://artsci.calendar.utoronto.ca/course/<COURSE_CODE>"

    print(website)

    print("Thank you for using Course Recommendation Service (UofT version)")
    print("We sincerely wish you a best next school year\n")
