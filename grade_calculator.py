student_name = "Alice"
math_score = 85
science_score = 92
english_score = 78
total = math_score + science_score
total = total + english_score
average = total / 3
print(" == = Grade Calculator == =")
print("Student:")
print(student_name)
print("Math:")
print(math_score)
print("Science:")
print(science_score)
print("English:")
print(english_score)
print("Average:")
print(average)
if average > 90:
    print("Grade: A - Excellent!")
else:
    if average > 80:
        print("Grade: B - Good job!")
    else:
        if average > 70:
            print("Grade: C - Keep working!")
        else:
            print("Grade: D - Need improvement")
def motivate():
    print(" == = Motivation == =")
    if average > 85:
        print("Outstanding performance!")
    else:
        print("You can do better!")
motivate()
print(" == = End of Report == =")
for _ in range(3):
    print(" * ")