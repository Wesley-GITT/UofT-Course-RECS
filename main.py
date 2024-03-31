"""
w
"""
import base
# Note: You may add helper functions, classes, etc. here as needed

def __input_similar_helper(item: str, set_to_find: set[str]) -> str:
    """Helper function. Print if the input item is similar to one another."""
    for _item in set_to_find:
        if item in _item or _item in item:
            return _item

    return ""

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
                print(f"Did you mean {similar_str}?")
            else:
                print(f"{choice} is not a/an {input_kind} in our dataset.")

    print(f"Your input on {input_kind}: {list(mset)}")
    return list(mset)

# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    g = base.load_graph("dataset/review_full.csv", "dataset/course.csv")
    print("Welcome to the Course Recommendation Service(UofT version)")
    name = input("Please enter your name to continue: ")
    print("Hi, " + name + ". You can now enter the courses you have completed or is taking this year\n")
    print("Enter the course you have taken or is taking.\nEnter one course code each time and press ENTER.\nIf you are DONE, enter DONE and type ENTER to continue.")
    courses = __input_helper(g, "course")

    print("\nEnter the programme you will be or is in.\nEnter programme code each time and press ENTER.\nIf you are DONE, enter DONE and type ENTER to continue.")
    programme_filter = __input_helper(g, "programme")
    recommendation = g.recommend_courses(courses, programme_filter)

    print("The recommendation course we would like to provides to you is follows")
    print("We have recommend three courses for the each course you entered")
    print(recommendation)

    print("\nFor further information on pre-requisite courses and co-requisite course,")
    print("please view the following websites we provided")

    website = f"https://artsci.calendar.utoronto.ca/course/<COURSE_CODE>"

    print(website)

    print("Thank you for using Course Recommendation Service (UofT version)")
    print("We sincerely wish you a best next school year\n")
