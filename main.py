from student import Topic


topic = Topic(
    name="A* Search",
    mastery=35,
    difficulty=8,
    days_to_exam=3
)

print(f"Initial mastery: {topic.mastery}%")

topic.update_mastery(45)

print("\nAfter Quiz 1")
print(f"Quiz history: {topic.quiz_history}")
print(f"Mastery: {topic.mastery}%")
print(f"Trend: {topic.get_performance_trend()}")

topic.update_mastery(62)

print("\nAfter Quiz 2")
print(f"Quiz history: {topic.quiz_history}")
print(f"Mastery: {topic.mastery}%")
print(f"Trend: {topic.get_performance_trend()}")

topic.update_mastery(80)

print("\nAfter Quiz 3")
print(f"Quiz history: {topic.quiz_history}")
print(f"Mastery: {topic.mastery}%")
print(f"Trend: {topic.get_performance_trend()}")