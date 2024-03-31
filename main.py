"""
w
"""
import baseClass
# Note: You may add helper functions, classes, etc. here as needed

# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    v = baseClass.load_graph(..., ...)
    print("Welcome to the Course Recommendation Service(UofT version)")
    name = input("Please enter your name to continue: ")
    print("hi, " + name + ". You can now enter your courses completed this year, ")
    print("enter one course in the form of CSC111 and press return, enter 0 as you finish")
    # choice = input("\nEnter course: ").lower()
    lst = []
    choice = 1
    while choice != '0':
        choice = input("\nEnter course: ").lower()
        if choice != '0':
            lst.append(choice)
    if choice == "0":
        print(lst)

    print("Now, please enter your programme? ")
    print("if you are a year one, enter one programme you are interested in")
    choice = input("\nEnter programme: ").lower()
    v = baseClass.Graph()
    v.recommend_courses()
    programme_choice = choice
    print(choice)

    recommendation = v.recommend_courses(lst, lst)

    print("The recommendation course we would like to provides to you is follows")
    print("We have recommend three courses for the each course you entered")
    print(recommendation)

    print("For further information on pre-requisite courses and co-requisite course,")
    print("please view the following websites we provided")

    website = ...

    print(website)

    print("Thank you for using Course Recommendation Service(UofT version)")
    print("We sincerely wish you a best next school year")
