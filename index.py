import os

def show_menu():
    print("\n===== OASIS INFOBYTE PYTHON INTERNSHIP PROJECTS =====")
    print("1. Voice Assistant")
    print("2. BMI Calculator (GUI)")
    print("3. Password Generator (GUI)")
    print("4. Exit")

while True:
    show_menu()
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        os.system("python Voice_Assistant/main.py")
    elif choice == "2":
        os.system("python BMI_Calculator/main.py")
    elif choice == "3":
        os.system("python Password_Generator/main.py")
    elif choice == "4":
        print("Exiting... Thank you!")
        break
    else:
        print("Invalid choice. Please try again.")
