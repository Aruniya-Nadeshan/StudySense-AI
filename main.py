from student import Student, Topic
from study_planner import StudyPlanner


student = Student(
    name="Niya",
    available_study_minutes=120
)

a_star = Topic(
    name="A* Search",
    mastery=35,
    difficulty=8,
    days_to_exam=3
)

fuzzy_logic = Topic(
    name="Fuzzy Logic",
    mastery=75,
    difficulty=6,
    days_to_exam=3
)

intelligent_agents = Topic(
    name="Intelligent Agents",
    mastery=55,
    difficulty=7,
    days_to_exam=3
)

student.add_topic(a_star)
student.add_topic(fuzzy_logic)
student.add_topic(intelligent_agents)

planner = StudyPlanner()


def display_plan(title):
    print(f"\n{title}")
    print("-" * len(title))

    study_plan = planner.create_plan(student)

    for index, item in enumerate(study_plan, start=1):
        print(
            f"{index}. {item['topic']} "
            f"- Priority: {item['priority']} "
            f"- Study Time: {item['minutes']} minutes"
        )


# Initial plan
display_plan("BEFORE QUIZ")

print(f"\nA* Search mastery before quiz: {a_star.mastery}%")

# Student completes a quiz and scores 80%
a_star.update_mastery(80)

print(f"A* Search mastery after quiz: {a_star.mastery}%")

# Generate a new plan after the agent observes the new performance
display_plan("AFTER QUIZ")