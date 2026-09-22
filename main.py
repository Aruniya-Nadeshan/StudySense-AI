from student import Student, Topic
from agent import StudyAgent


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

agent = StudyAgent()

ranked_topics = agent.rank_topics(student.topics)

print("\nStudy Priority Ranking\n")

for index, topic in enumerate(ranked_topics, start=1):
    priority = agent.calculate_priority(topic)

    print(
        f"{index}. {topic.name} "
        f"- Priority Score: {priority}"
    )