score= int(input("Enter the student's score:"))

if score >=85:
    Grade="A"
    print("Brillant Work!")
elif score>=75:
    Grade="B"
    print("well Done!")
elif score>=60:
    Grade="C"
    print("Satisfactory work!")
elif score>=55:
    Grade="D"
    print("More Efforts Needed!")
else:
    Grade="F"
    print("Failed!")

print(f"The student's grade is {Grade}")

   