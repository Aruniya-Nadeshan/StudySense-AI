from student import Student, Topic
from study_planner import StudyPlanner


student = Student(
    name="Niya",
    available_study_minutes=120
)

student.add_topic(
    Topic(
        name="A* Search",
        mastery=35,
        difficulty=8,
        days_to_exam=3
    )
)

student.add_topic(
    Topic(
        name="Fuzzy Logic",
        mastery=75,
        difficulty=6,
        days_to_exam=3
    )
)

student.add_topic(
    Topic(
        name="Intelligent Agents",
        mastery=55,
        difficulty=7,
        days_to_exam=3
    )
)

planner = StudyPlanner()

study_plan = planner.create_plan(student)

print(f"\nStudy Plan for {student.name}")
print(f"Available Time: {student.available_study_minutes} minutes\n")

for index, item in enumerate(study_plan, start=1):
    print(
        f"{index}. {item['topic']} "
        f"- Priority: {item['priority']} "
        f"- Study Time: {item['minutes']} minutes"
    )