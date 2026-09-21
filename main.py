from student import Student, Topic


student = Student(
    name="Niya",
    available_study_minutes=120
)

topic1 = Topic(
    name="A* Search",
    mastery=35,
    difficulty=8,
    days_to_exam=3
)

student.add_topic(topic1)

print(student)
print(student.topics)