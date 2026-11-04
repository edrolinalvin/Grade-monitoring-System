student_ids = []       
student_names = []     
student_subjects = []  
student_scores = []
student_pins = []     

TEACHER_PASSWORD = "FB1-BSIT1-04"  
MAX_TRIES = 3    


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_score(subject_name):
    while True:
        raw_input_value = input(f"Enter score for {subject_name} (0-100): ")
        try:
            score = float(raw_input_value)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if is_valid_score(score):
            return score
        print("Invalid score. Must be between 0 and 100.")


def is_valid_score(score):
    return score >= 0 and score <= 100


def is_valid_id(student_id):
    """ID format: 2 digits, 4 digits, 6 digits separated by dashes (example 02-2627-010787)."""
    parts = student_id.split("-")
    if len(parts) != 3:
        return False
    if len(parts[0]) != 2 or len(parts[1]) != 4 or len(parts[2]) != 6:
        return False
    for part in parts:
        if not part.isdigit():
            return False
    return True


def get_student_id(prompt):
    """Keeps asking until the ID follows the format 00-0000-000000."""
    while True:
        student_id = input(prompt).strip()
        if is_valid_id(student_id):
            return student_id
        print("Invalid ID. Use numbers only in this format: 02-2627-010787")


def get_new_pin():
    """Keeps asking until the PIN is exactly 4 digits."""
    while True:
        pin = input("Set a 4 digit PIN for the student: ").strip()
        if len(pin) == 4 and pin.isdigit():
            return pin
        print("Invalid PIN. It must be exactly 4 numbers.")


def find_student(student_id):
    """Returns the position of the student in the lists, or -1 if not found."""
    for i in range(len(student_ids)):
        if student_ids[i] == student_id:
            return i
    return -1


def compute_average(scores):
    total = 0
    for score in scores:
        total = total + score
    return total / len(scores)


def get_grade_equivalent(average):
    if average >= 94:
        return "1.00"
    elif average >= 83:
        return "1.50"
    elif average >= 74:
        return "2.00"
    elif average >= 61:
        return "2.50"
    elif average >= 50:
        return "3.00"
    else:
        return "No Credit"


def check_pass_fail(average):
    if average >= 50:
        status = "Passed"
        if average < 55:
            status += " (warning, needs improvement)"
    else:
        status = "No Credit (needs improvement)"
    return status


def count_scores_with_while(scores):
    count = 0
    index = 0
    while index < len(scores):
        if scores[index] >= 90:
            count = count + 1
        index = index + 1
    return count


def show_grade_report(position):
    """Prints the grade report of the student at this position, subjects as columns."""
    subjects = student_subjects[position]
    scores = student_scores[position]

    if len(scores) == 0:
        print("\nNo grades entered yet.\n")
        return

    average = compute_average(scores)
    if average >= 50:
        status = "Passed"
    else:
        status = "No Credit"

    header = f"{'ID NUMBER':<16} | {'STUDENT NAME':<20}"
    row = f"{student_ids[position]:<16} | {student_names[position]:<20}"

    for i in range(len(subjects)):
        header += f" | {subjects[i]:<10}"
        row += f" | {scores[i]:<10}"

    header += f" | {'AVERAGE':<8} | {'STATUS':<10} | {'EQ GRADE':<9}"
    row += f" | {average:<8.2f} | {status:<10} | {get_grade_equivalent(average):<9}"

    line = "=" * len(header)
    print("\n" + line)
    print(header)
    print(line)
    print(row)
    print(line)

    if status == "No Credit":
        print("Needs improvement.")
    elif average < 55:
        print("warning, needs improvement.")
    print("Subjects with score 90 or above:", count_scores_with_while(scores))
    print()


# ==========================================================
# TEACHER FUNCTIONS
# ==========================================================

def add_student():
    student_id = get_student_id("Enter student ID: ")
    if student_id == "":
        print("ID cannot be empty.\n")
        return
    if find_student(student_id) != -1:
        print("That ID already exists.\n")
        return

    name = input("Enter student name: ").strip()
    pin = get_new_pin()
    student_ids.append(student_id)
    student_names.append(name)
    student_pins.append(pin)
    student_subjects.append([])
    student_scores.append([])
    print(f"Student {name} added.\n")


def enter_grade():
    student_id = get_student_id("Enter student ID: ")
    position = find_student(student_id)
    if position == -1:
        print("Student ID not found.\n")
        return

    subject_name = input("Enter subject name: ").strip()
    if subject_name in student_subjects[position]:
        print("Subject already has a grade. Use Edit Grade instead.\n")
        return

    score = get_score(subject_name)
    student_subjects[position].append(subject_name)
    student_scores[position].append(score)
    print("Grade saved.\n")


def view_all_students():
    if len(student_ids) == 0:
        print("No students yet.\n")
        return

    all_subjects = []
    for i in range(len(student_subjects)):
        for subject in student_subjects[i]:
            if subject not in all_subjects:
                all_subjects.append(subject)

    # header
    header = f"{'ID NUMBER':<16} | {'STUDENT NAME':<20}"
    for subject in all_subjects:
        header += f" | {subject:<10}"
    header += f" | {'AVERAGE':<8} | {'STATUS':<10} | {'EQ GRADE':<9}"

    line = "=" * len(header)
    print("\n" + line)
    print(header)
    print(line)

    # one row per student
    for i in range(len(student_ids)):
        row = f"{student_ids[i]:<16} | {student_names[i]:<20}"

        for subject in all_subjects:
            if subject in student_subjects[i]:
                score = student_scores[i][student_subjects[i].index(subject)]
                row += f" | {score:<10}"
            else:
                row += f" | {'':<10}"

        if len(student_scores[i]) == 0:
            row += f" | {'':<8} | {'No grades':<10} | {'':<9}"
        else:
            average = compute_average(student_scores[i])
            if average >= 50:
                status = "Passed"
            else:
                status = "No Credit"
            row += f" | {average:<8.2f} | {status:<10} | {get_grade_equivalent(average):<9}"

        print(row)
    print(line + "\n")


def edit_grade():
    student_id = get_student_id("Enter student ID: ")
    position = find_student(student_id)
    if position == -1:
        print("Student ID not found.\n")
        return

    if len(student_scores[position]) == 0:
        print("This student has no grades yet.\n")
        return

    for i in range(len(student_subjects[position])):
        print(f"{i + 1}. {student_subjects[position][i]}: {student_scores[position][i]}")

    choice = input("Enter subject number to edit: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(student_subjects[position]):
        print("Invalid choice.\n")
        return

    index = int(choice) - 1
    new_score = get_score(student_subjects[position][index])
    student_scores[position][index] = new_score
    print("Grade updated.\n")


def remove_student():
    student_id = get_student_id("Enter student ID: ")
    position = find_student(student_id)
    if position == -1:
        print("Student ID not found.\n")
        return

    confirm = input(f"Remove {student_names[position]}? (yes or no): ").strip().lower()
    if confirm == "yes":
        student_ids.pop(position)
        student_names.pop(position)
        student_pins.pop(position)
        student_subjects.pop(position)
        student_scores.pop(position)
        print("Student removed.\n")
    else:
        print("Cancelled.\n")


# ==========================================================
# TEACHER MENU
# ==========================================================

def teacher_menu():
    while True:
        print("=== Teacher Menu ===")
        print("1. Add Student")
        print("2. Enter Student Grade")
        print("3. View All Students")
        print("4. Edit Grade of Student")
        print("5. Remove Student")
        print("0. Back")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            enter_grade()
        elif choice == "3":
            view_all_students()
        elif choice == "4":
            edit_grade()
        elif choice == "5":
            remove_student()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.\n")


# ==========================================================
# STUDENT MENU
# ==========================================================

def student_menu():
    current_position = -1 

    while True:
        print("=== Student Menu ===")
        print("1. Type ID and PIN")
        print("2. View Grade")
        print("3. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            student_id = get_student_id("Enter your ID: ")
            position = find_student(student_id)
            current_position = -1
            if position == -1:
                print("Student ID not found.\n")
            else:
                tries = 0
                while tries < MAX_TRIES:
                    pin = input("Enter your PIN: ").strip()
                    if pin == student_pins[position]:
                        current_position = position
                        print(f"Login successful. Welcome, {student_names[position]}.\n")
                        break
                    tries = tries + 1
                    remaining = MAX_TRIES - tries
                    if remaining > 0:
                        print(f"Wrong PIN. {remaining} tries left.")
                if current_position == -1:
                    print("Too many wrong tries. Access denied.\n")
        elif choice == "2":
            if current_position == -1:
                print("Please log in first (option 1).\n")
            else:
                show_grade_report(current_position)
        elif choice == "3":
            break
        else:
            print("Invalid option. Please try again.\n")


# ==========================================================
# TEACHER LOGIN
# ==========================================================

def teacher_login():
    """Asks for the teacher password. Returns True if correct, False after 3 wrong tries."""
    tries = 0
    while tries < MAX_TRIES:
        password = input("Enter teacher password: ")
        if password == TEACHER_PASSWORD:
            print("Login successful.\n")
            return True
        tries = tries + 1
        remaining = MAX_TRIES - tries
        if remaining > 0:
            print(f"Wrong password. {remaining} tries left.")
    print("Too many wrong tries. Access denied.\n")
    return False


# ==========================================================
# MAIN MENU
# ==========================================================

def main():
    while True:
        print("=== Grade Monitoring System ===")
        print("1. Teacher")
        print("2. Student")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            if teacher_login():
                teacher_menu()
        elif choice == "2":
            student_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")


if __name__ == "__main__":
    main()