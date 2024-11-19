import matplotlib.pyplot as plt
import data
import os

def clean_assignments():
    with open("data/assignments.txt", "r") as file:
        assignments_raw = file.read()

    assignments_list = assignments_raw.split("\n")
    assignments_db = {}

    for i in range(len(assignments_list) // 3):
        assignments_db.update({assignments_list[3*i]: (assignments_list[3*i+1], assignments_list[3*i+2])})

    assignments_id = {}
    for i in range(len(assignments_list) // 3):
        assignments_id.update({assignments_list[3*i+1]: assignments_list[3*i+2]})

    return assignments_db, assignments_id

def clean_students():
    with open("data/students.txt", "r") as file:
        students_raw = file.read()

    students_list = students_raw.split("\n")
    students_db = {}

    for i in students_list:
        students_db.update({i[3:]:i[0:3]})

    return students_db

def clean_submissions():
    subs_raw = os.listdir("data/submissions")
    subs_list = []
    for i in subs_raw:
        with open("data/submissions/" + i, "r") as file:
            content = file.read()
        subs_list.append(tuple(content.split("|")))
    subs_dict = {}
    for i in subs_list:
        if i[0] in subs_dict.keys():
            subs_dict[i[0]].append((i[1],i[2]))
        else:
            subs_dict.update({i[0]:[(i[1],i[2])]})
    subs_id = {}
    for i in subs_list:
        if i[1] in subs_id.keys():
            subs_id[i[1]].append(i[2])
        else:
            subs_id.update({i[1]:[i[2]]})

    return subs_dict, subs_id

menu = "1. Student grade\n2. Assignment statistics\n3. Assignment graph\n"
students = clean_students()
assignments, assignments_byid = clean_assignments()
submissions_students, submissions_assignments = clean_submissions()

def main():
    print(menu)
    selection = input("Enter your selection: ")

    if selection == "1":
        student = input("What is the student's name: ")
        if student not in students.keys():
            print("Student not found")
        else:
            points = 0
            for i in submissions_students[students[student]]:
                points += (float(assignments_byid[i[0]]) * (float(i[1])/100))
            print(f"{int(points/10)}%\n")

    elif selection == "2":
        assign = input("What is the assignment name: ")
        if assign not in assignments.keys():
            print("Assignment not found")
        else:
            asl = submissions_assignments[assignments[assign][0]]
            asl = [int(i) for i in asl]
            print(f"Min: {min(asl)}%")
            print(f"Avg: {sum(asl)//len(asl)}%")
            print(f"Max: {max(asl)}%\n")

    elif selection == "3":
        assign = input("What is the assignment name: ")
        if assign not in assignments.keys():
            print("Assignment not found")
            print("")
        else:
            asl = submissions_assignments[assignments[assign][0]]
            asl = [int(i) for i in asl]
            plt.hist(asl, bins=[40, 50, 60, 70, 80, 90, 100])
            plt.show()



main()
