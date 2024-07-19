import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox

class Course:
    def __init__(self, root):
        self.root = root
        self.root.title("Timetable")
        self.root.geometry("1000x650")
        self.root.configure(bg="#778899")

        self.file_label = tk.Label(root, text="Enter the file path:", fg="white", bg="#778899", font=("Times New Roman", 13))
        self.file_label.grid(row=1, column=1, pady=20)

        self.input_entry = tk.Entry(root, width=30)
        self.input_entry.grid(row=1, column=2)

        self.year_label = tk.Label(root, text="Year:", fg="white", bg="#778899", font=("Times New Roman", 13))
        self.year_label.grid(row=4, column=1, sticky="e")

        self.years = ["1", "2", "3", "4", "5"]
        self.selected_year = tk.StringVar()
        self.year_dropdown = ttk.Combobox(root, textvariable=self.selected_year, values=self.years, width=10)
        self.year_dropdown.grid(row=4, column=2, padx=5, pady=5, sticky="w")

        self.departament_label = tk.Label(root, text="Departament:", fg="white", bg="#778899", font=("Times New Roman", 13))
        self.departament_label.grid(row=4, column=3, padx=5, sticky="e")

        self.departments = ["CHI", "CS", "ECE", "ECON", "EE", "EECS", "ENGR", "FRE", "GER", "IE", "ISE", "LIFE", "MATH", "MGT", "UNI"]
        self.selected_department = tk.StringVar()
        self.department_dropdown = ttk.Combobox(root, textvariable=self.selected_department, values=self.departments, width=20)
        self.department_dropdown.grid(row=4, column=4, padx=5, pady=5, sticky="w")

        self.button_frame = tk.Frame(root, bg="#778899")
        self.button_frame.grid(row=7, column=0, columnspan=4, pady=40)

        self.display_button = tk.Button(self.button_frame, width=10, text="Display", bg="#3CB371", fg="white", command=self.display_courses)
        self.display_button.grid(row=0, column=0, padx=5)

        self.clear_button = tk.Button(self.button_frame, width=10, text="Clear", bg="#FF8C00", fg="white", command=self.clear_courses)
        self.clear_button.grid(row=0, column=1, padx=5)

        self.save_button = tk.Button(self.button_frame, width=10, text="Save", bg="#4169E1", fg="white", command=self.save_courses)
        self.save_button.grid(row=0, column=2, padx=5)

        self.warnings_label = tk.Label(root, text="Selected Courses:", fg="white", bg="#778899", font=("Times New Roman", 13))
        self.warnings_label.grid(row=9, column=1, padx=(20, 20), pady=5, sticky="w")

        self.warnings_listbox = tk.Listbox(root, height=22, width=50)
        self.warnings_listbox.grid(row=10, column=0, padx=(25, 20), pady=5, columnspan=3, sticky="w")

        self.courses_label = tk.Label(root, text="Courses:", fg="white", bg="#778899", font=("Times New Roman", 13))
        self.courses_label.grid(row=9, column=3, padx=(25, 20), pady=5, sticky="w")

        self.selected_courses = []
        self.courses_listbox = tk.Listbox(root, height=22, width=100)
        self.courses_listbox.grid(row=10, column=3, padx=(25, 20), pady=5, columnspan=3, sticky="w")
        self.courses_listbox.bind("<<ListboxSelect>>", self.select_course)



    def read_csv_file(self, file_path):
        courses = []
        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    courses.append(row)
        except FileNotFoundError:
            messagebox.showinfo("File not found", "The specified CSV file was not found. Please check the file path and try again.")
        return courses

    def display_courses(self):
        file_path = self.input_entry.get()
        year = self.selected_year.get()
        department = self.selected_department.get()

        self.courses_listbox.delete(0, tk.END)

        if not file_path:
            messagebox.showinfo("File Path Required", "Please enter the file path.")
        else:
            courses = self.read_csv_file(file_path)
            filtered_courses = []

            for course in courses:
                course_info = course[0].split(',')
                course_department = course_info[0].split()[0]
                course_year = course_info[0].split()[1]

                if (not year or course_year.startswith(year)) and (not department or department == course_department):
                    filtered_courses.append(course)

            if not filtered_courses:
                messagebox.showinfo("No Courses Found", "No courses found for the selected criteria.")
            else:
                for course in filtered_courses:
                    course_str = ','.join(course)
                    if course_str not in self.selected_courses:
                        self.courses_listbox.insert(tk.END, course_str)

    def clear_courses(self):
        self.courses_listbox.delete(0, tk.END)
        self.warnings_listbox.delete(0, tk.END)
        self.selected_courses.clear()

    def save_courses(self):
        if not self.selected_courses:
            messagebox.showinfo("No Courses Selected", "There are no courses selected to save.")
        else:
            with open("timetable.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                for course in self.selected_courses:
                    writer.writerow([course])
            messagebox.showinfo("Saved", "Timetable saved successfully to timetable.csv.")

    def time_conflict(self, new_course_info):
        new_course_days = new_course_info[2].split()
        new_course_times = new_course_info[3].split()


        for course in self.selected_courses:
            course_info = course.split(',')
            course_days = course_info[2].split()
            course_times = course_info[3].split()


            for new_day, new_time in zip(new_course_days, new_course_times):
                for course_day, course_time_entry in zip(course_days, course_times):
                    if course_day == new_day:
                        if self.time_conflict_exists(new_time, course_time_entry):
                            print(f"Konflikt orari gjetur: {new_course_info[0]} dhe {course_info[0]} në ditën {new_day}")
                            return True
        return False

    def time_conflict_exists(self, new_time, course_time_entry):
        new_start_time, new_end_time = new_time.split('-')
        course_start_time, course_end_time = course_time_entry.split('-')

        if new_start_time < course_end_time and new_end_time > course_start_time:
            return True

        return False

    def select_course(self, event):
        selected_index = self.courses_listbox.curselection()
        if selected_index:
            selected_course = self.courses_listbox.get(selected_index)
            new_course_info = selected_course.split(',')

            if selected_course in self.selected_courses:
                messagebox.showinfo("Course Already Added", f"The course {new_course_info[0]} has already been added.")
            else:
                if len(self.selected_courses) >= 6:
                    messagebox.showinfo("Cannot add department code","The maximum number of courses (6) has been reached.")

                elif self.time_conflict(new_course_info):
                    messagebox.showinfo("Time Conflict", f"Time conflict detected for {new_course_info[0]}. Course cannot be added.")
                else:
                    self.selected_courses.append(selected_course)
                    self.warnings_listbox.insert(tk.END, f"Added {new_course_info[0]}")





root = tk.Tk()
app = Course(root)
root.mainloop()


