import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import string
from datetime import datetime, timedelta


class Student:
    def __init__(self, name, email):
        self.__student_id = self.gen_student_id()
        self.__name = name
        self.__email = email
        self.__registered_modules = []
        self.__preferences = []
        self.__registered_date = {}

    def gen_student_id(self):
        prefix = random.choice(["ST", "UN", "TE"])
        return f"{prefix}{''.join(random.choices(string.digits, k=4))}"

    def get_student_id(self):
        return self.__student_id

    def get_name(self):
        return self.__name

    def get_registered_modules(self):
        return self.__registered_modules.copy()

    def get_preferences(self):
        return self.__preferences.copy()

    def add_preferences(self, category):
        if category not in self.__preferences:
            self.__preferences.append(category)

    def modules_register(self, course_id):
        if course_id not in self.__registered_modules:
            self.__registered_modules.append(course_id)
            self.__registered_date[course_id] = datetime.now()
            return True
        return False

    def is_registered(self, course_id):
        return course_id in self.__registered_modules

    def course_review(self, course_id, rating, comment=""):
        if course_id in self.__registered_modules:
            return {
                'student_id': self.__student_id,
                'student_name': self.__name,
                'rating': rating,
                'comment': comment,
                'date': datetime.now()
            }
        return None

    def get_registered_cou(self):
        return len(self.__registered_modules)


class Course:
    def __init__(self, title, description, instructor_id, category, price=0.0):
        self.__course_id = self.gen_course_id()
        self.__title = title
        self.__description = description
        self.__instructor_id = instructor_id
        self.__category = category
        self.__ratings = []
        self.__price = price
        self.__reviews = []
        self.__enrolled_students = []
        self.__create_date = datetime.now()

    def gen_course_id(self):
        prefix = random.choice(["CO", "ED"])
        return f"{prefix}{''.join(random.choices(string.digits, k=5))}"

    def get_course_id(self):
        return self.__course_id

    def get_title(self):
        return self.__title

    def get_category(self):
        return self.__category

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.__ratings.append(rating)

    def add_review(self, review):
        self.__reviews.append(review)

    def register_student(self, student_id):
        if student_id not in self.__enrolled_students:
            self.__enrolled_students.append(student_id)

    def get_avg_rating(self):
        return sum(self.__ratings) / len(self.__ratings) if self.__ratings else 0

    def get_registered_cou(self):
        return len(self.__enrolled_students)

    def get_review_cou(self):
        return len(self.__reviews)

    def managing(self):
        return {
            'course_id': self.__course_id,
            'title': self.__title,
            'average_rating': round(self.get_avg_rating(), 2),
            'enrolled_students': len(self.__enrolled_students),
            'category': self.__category
        }


class Recommendation:
    
    def __init__(self, student_info, course_view):
        self.__student_info = student_info
        self.__course_view = course_view
    
    
    def preferences_score(self, course, student):
        score = 0
        if course.get_category() in student.get_preferences():
            score += 50
        return score
    
    def quality_score(self, course):
        rating = course.get_avg_rating()
        return rating * 5
    
    def popularity_score(self, course):
        enrolled = course.get_registered_cou()
        popularity = min(enrolled / 10, 1.5) * 10
        return popularity
    
    def last_score(self, course):
        days_since_creation = (datetime.now() - course.get_creation_date()).days
        if days_since_creation < 30:
            return 10
        return 0
    
    def gen_recommend(self, all_courses, student):
        recommendations = []
        enrolled_course_ids = student.get_registered_modules()
        
        # filter out already enrolled courses
        available_courses = []
        for i in all_courses:
            if i.get_course_id() not in enrolled_course_ids:
                available_courses.append(i)
        
        scored_courses = []
        for course in available_courses:
            total_score = 0.0
            total_score += self.preferences_score(course, student)
            total_score += self.quality_score(course)
            total_score += self.popularity_score(course)
            total_score += self.last_score(course)
            
            scored_courses.append((course, total_score))
        
        # sorting by score and return top 5
        scored_courses.sort(key=lambda x: x[1], reverse=True)
        recommendations = [course for course, score in scored_courses[:5]]
        return recommendations


class Instructor:
    def __init__(self, name, email, expertise):
        self.__instructor_id = self.gen_instructor_id()
        self.__name = name
        self.__email = email
        self.__expertise = expertise
        self.__manage_courses = []

    def gen_instructor_id(self):
        return f"INS{''.join(random.choices(string.digits, k=6))}"

    def get_instructor_id(self):
        return self.__instructor_id

    def create_course(self, title, description, category, price):
        course = Course(title, description, self.__instructor_id, category, price)
        self.__manage_courses.append(course.get_course_id())
        return course

    def manage_course(self, course_id):
        if course_id not in self.__manage_courses:
            self.__manage_courses.append(course_id)


class Admin:
    def __init__(self):
        self.__students = {}
        self.__instructors = {}
        self.__courses = {}
        self.__admin_key = "admin"
        self.__activity = []
    
    def activities(self, message):
        activity_log = {
            'timestamp': datetime.now(),
            'message': message
        }
        self.__activity.append(activity_log)
    
    def get_student(self, student_id):
        return self.__students.get(student_id)
    
    def get_instructor(self, instructor_id):
        return self.__instructors.get(instructor_id)
    
    def get_course(self, course_id):
        return self.__courses.get(course_id)
    
    def get_all_courses(self):
        return list(self.__courses.values())
    
    def get_all_students(self):
        return list(self.__students.values())
    
    def verify_admin_key(self, key):
        return key == self.__admin_key
    
    def register_student(self, name, email):
        new_student = Student(name, email)
        self.__students[new_student.get_student_id()] = new_student
        log_msg = f"Student {name} registered with ID {new_student.get_student_id()}"
        self.activities(log_msg)
        return new_student
    
    def register_instructor(self, name, email, expertise):
        new_instructor = Instructor(name, email, expertise)
        self.__instructors[new_instructor.get_instructor_id()] = new_instructor
        self.activities(f"Instructor {name} registered")
        return new_instructor
    
    def enroll_course(self, course):
        self.__courses[course.get_course_id()] = course
        self.activities(f"Course '{course.get_title()}' added")
    
    def enroll_student(self, student_id, course_id):
        student = self.__students.get(student_id)
        course = self.__courses.get(course_id)
        
        if student and course:
            if student.modules_register(course_id):
                course.register_student(student_id)
                x_sc = self.activities(f"Student {student_id} enrolled in {course_id}")
        return x_sc
    
    def submit_review(self, student_id, course_id, rating, comment=""):
        student = self.__students.get(student_id)
        course = self.__courses.get(course_id)
        
        if student and course:
            review = student.course_review(course_id, rating, comment)
            if review:
                course.add_review(review)
                course.add_rating(rating)
                x_rev =  self.activities(f"Student {student_id} reviewed course {course_id}")
        return x_rev
    
    def get_recommendations(self, student_id):
        student = self.__students.get(student_id)
        if student:
            recommender = Recommendation()
            recommendations = recommender.gen_recommend(student_id, list(self.__courses.values()), student)
            return recommendations
        return []
    
    def get_report(self, days=10):
        for_date = datetime.now() - timedelta(days=days)

        enrollments = [
            {'student': i.get_name(),
             'course': self.__courses.get(i_id).get_title() 
            if self.__courses.get(i_id) else 'Unknown','date': date}
            
            for i in self.__students.values()
            for i_id, date in i.get_enrollment_dates().items()
            if date >= for_date]

        return {
            'period': f'Last {days} days',
            'total_enrollments': len(enrollments),
            'enrollments': enrollments
        }

    
    def get_board(self, top_n=10):
        course_rank = []
        for course in self.__courses.values():
            avg_rating = course.get_avg_rating()
            if avg_rating > 0:
                course_data = {
                    'course_id': course.get_course_id(),
                    'title': course.get_title(),
                    'average_rating': round(avg_rating, 2),
                    'total_ratings': len(course.get_ratings()),
                    'enrolled_students': course.get_registered_cou()
                }
                course_rank.append(course_data)
        
        course_rank.sort(key=lambda x: (x['average_rating'], x['total_ratings']), reverse=True)
        return course_rank[:top_n]
    
    def get_system_view(self):
        total_enrollments = 0
        for s in self.__students.values():
            total_enrollments += s.get_registered_cou()
        
        total_reviews = 0
        for c in self.__courses.values():
            total_reviews += c.get_review_cou()
        
        system_stats = {
            'total_students': len(self.__students),
            'total_instructors': len(self.__instructors),
            'total_courses': len(self.__courses),
            'total_enrollments': total_enrollments,
            'total_reviews': total_reviews
        }
        return system_stats


# GUI Application
class GUI:
    def __init__(self, manager):
        self.manager = manager
        self.window = tk.Tk()
        self.window.title("online education platform")
        self.window.geometry("860x600")
        self.window.configure(bg="#f5f5f5")
        self.admin_log_in = False

        # styling
        self.setup_styles()
        
        # create notebook for tabs
        self.tab_control = ttk.Notebook(self.window)
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        self.init_tabs()
        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_enrollment_tab()
        self.create_recommendations_tab()
        self.create_dashboard_tab()
        self.create_report_tab()
        self.create_admin_tab()

    def setup_styles(self):
        style = ttk.Style(self.window)
        style.theme_use('clam')
        style.configure("TNotebook.Tab", font=('Arial', 12, 'bold'), padding=[10, 5])
        style.configure("TButton", font=('Arial', 11, 'bold'), padding=5)
        style.configure("TLabel", font=('Arial', 11))
        style.configure("TEntry", font=('Arial', 11))

    def init_tabs(self):
        self.tab_students = ttk.Frame(self.tab_control)
        self.tab_instructors = ttk.Frame(self.tab_control)
        self.tab_courses = ttk.Frame(self.tab_control)
        self.tab_enrollment = ttk.Frame(self.tab_control)
        self.tab_recommendations = ttk.Frame(self.tab_control)
        self.tab_dashboard = ttk.Frame(self.tab_control)
        self.tab_reports = ttk.Frame(self.tab_control)
        self.tab_admin = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_students, text="Students")
        self.tab_control.add(self.tab_instructors, text="Instructors")
        self.tab_control.add(self.tab_courses, text="Courses")
        self.tab_control.add(self.tab_enrollment, text="Enrollment")
        self.tab_control.add(self.tab_recommendations, text="Recommendations")
        self.tab_control.add(self.tab_dashboard, text="Dashboard")
        self.tab_control.add(self.tab_reports, text="Reports")
        self.tab_control.add(self.tab_admin, text="Admin")

    def create_student_tab(self):
        frame = ttk.Frame(self.tab_students, padding=20)
        frame.pack(pady=20)
        
        # labels
        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        
        # entry fields
        self.student_name_entry = ttk.Entry(frame, width=30)
        self.student_email_entry = ttk.Entry(frame, width=30)
        self.student_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.student_email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # buttons
        ttk.Button(frame, text="Register Student", command=self.register_student).grid(row=2, column=0, columnspan=2, pady=15)
        ttk.Button(frame, text="View Student Profile", command=self.view_student_profile).grid(row=3, column=0, columnspan=2, pady=10)

    def register_student(self):
        name = self.student_name_entry.get()
        email = self.student_email_entry.get()
        try:
            student = self.manager.register_student(name, email)
            msg = f"Student registered with ID: {student.get_student_id()}"
            messagebox.showinfo("Success", msg)
            self.student_name_entry.delete(0, tk.END)
            self.student_email_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def view_student_profile(self):
        student_id = simpledialog.askstring("Student Profile", "Enter Student ID:")
        if student_id:
            student = self.manager.get_student(student_id)
            if student:
                profile_text = f"Student ID: {student.get_student_id()}\n"
                profile_text += f"Name: {student.get_name()}\n"
                profile_text += f"Email: {student.get_email()}\n"
                profile_text += f"Enrolled Courses: {len(student.get_registered_modules())}\n"
                prefs = student.get_preferences()
                profile_text += f"Preferences: {', '.join(prefs) if prefs else 'None'}"
                messagebox.showinfo("Student Profile", profile_text)
            else:
                messagebox.showerror("Error", "Student not found")

    def create_instructor_tab(self):
        frame = ttk.Frame(self.tab_instructors, padding=20)
        frame.pack(pady=20)
        
        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        ttk.Label(frame, text="Expertise:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        
        self.instructor_name_entry = ttk.Entry(frame, width=30)
        self.instructor_email_entry = ttk.Entry(frame, width=30)
        self.instructor_expertise_entry = ttk.Entry(frame, width=30)
        
        self.instructor_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.instructor_email_entry.grid(row=1, column=1, padx=5, pady=5)
        self.instructor_expertise_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Register Instructor", command=self.register_instructor).grid(row=3, column=0, columnspan=2, pady=15)
        ttk.Button(frame, text="View Instructor Profile", command=self.view_instructor_profile).grid(row=4, column=0, columnspan=2, pady=10)

    def register_instructor(self):
        name = self.instructor_name_entry.get()
        email = self.instructor_email_entry.get()
        expertise = self.instructor_expertise_entry.get()
        try:
            instructor = self.manager.register_instructor(name, email, expertise)
            messagebox.showinfo("Successful", f"Instructor registered with ID: {instructor.get_instructor_id()}")
            self.instructor_name_entry.delete(0, tk.END)
            self.instructor_email_entry.delete(0, tk.END)
            self.instructor_expertise_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def view_instructor_profile(self):
        instructor_id = simpledialog.askstring("Instructor Profile", "Enter Instructor ID:")
        if instructor_id:
            instructor = self.manager.get_instructor(instructor_id)
            if instructor:
                profile_text = f"Instructor ID: {instructor.get_instructor_id()}\n"
                profile_text += f"Name: {instructor.get_name()}\n"
                profile_text += f"Email: {instructor.get_email()}\n"
                profile_text += f"Expertise: {instructor.get_expertise()}\n"
                profile_text += f"Managed Courses: {len(instructor.get_manage_course())}"
                messagebox.showinfo("Instructor Profile", profile_text)
            else:
                messagebox.showerror("Error", "Instructor not found")

    def create_course_tab(self):
        frame = ttk.Frame(self.tab_courses, padding=20)
        frame.pack(pady=20)
        
        labels = ["Title:", "Description:", "Category:", "Price:", "Instructor ID:"]
        self.course_entries = []
        for i, text in enumerate(labels):
            ttk.Label(frame, text=text).grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(frame, width=35)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.course_entries.append(entry)            
        
        ttk.Button(frame, text="Create Course", command=self.create_course).grid(row=5, column=0, columnspan=2, pady=15)
        ttk.Button(frame, text="Browse Courses", command=self.browse_courses).grid(row=6, column=0, columnspan=2, pady=10)

    def create_course(self):
        title = self.course_entries[0].get()
        desc = self.course_entries[1].get()
        category = self.course_entries[2].get()
        try:
            price = float(self.course_entries[3].get())
        except:
            price = 0
        instructor_id = self.course_entries[4].get()
        
        instructor = self.manager.get_instructor(instructor_id)
        if not instructor:
            messagebox.showerror("Error", "Invalid Instructor ID")
            return
        
        course = instructor.create_course(title, desc, category, price)
        self.manager.enroll_course(course)
        messagebox.showinfo("Success", f"Course created with ID: {course.get_course_id()}")
        
        for entry in self.course_entries:
            entry.delete(0, tk.END)
            
    def browse_courses(self):
        courses = self.manager.get_all_courses()
        if courses:
            course_list = "\n".join([f"{c.get_title()} (ID: {c.get_course_id()}) - {c.get_category()}" 
                                   for c in courses])
            messagebox.showinfo("Available Courses", course_list)
        else:
            messagebox.showinfo("Courses", "No courses available")

    def create_enrollment_tab(self):
        frame = ttk.Frame(self.tab_enrollment, padding=20)
        frame.pack(pady=20)
        
        ttk.Label(frame, text="Student ID:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        ttk.Label(frame, text="Course ID:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        
        self.enroll_student_entry = ttk.Entry(frame, width=30)
        self.enroll_course_entry = ttk.Entry(frame, width=30)
        self.enroll_student_entry.grid(row=0, column=1, padx=5, pady=5)
        self.enroll_course_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Enroll Student", command=self.enroll_student).grid(row=2, column=0, columnspan=2, pady=15)

    def enroll_student(self):
        student_id = self.enroll_student_entry.get()
        course_id = self.enroll_course_entry.get()
        
        if self.manager.enroll_student(student_id, course_id):
            messagebox.showinfo("Success", f"Student {student_id} enrolled in {course_id}")
            self.enroll_student_entry.delete(0, tk.END)
            self.enroll_course_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Enrollment failed. Check IDs.")

    def create_recommendations_tab(self):
        frame = ttk.Frame(self.tab_recommendations, padding=20)
        frame.pack(pady=20)
        
        ttk.Label(frame, text="Student ID:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.recommend_student_entry = ttk.Entry(frame, width=30)
        self.recommend_student_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Get Recommendations", command=self.get_recommendations).grid(row=1, column=0, columnspan=2, pady=15)
        
        self.recommendations_text = tk.Text(frame, height=15, width=80, font=('Arial', 11))
        self.recommendations_text.grid(row=2, column=0, columnspan=2, pady=10)

    def get_recommendations(self):
        student_id = self.recommend_student_entry.get()
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID")
            return
            
        student = self.manager.get_student(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found")
            return
            
        recommendations = self.manager.get_recommendations(student_id)
        self.recommendations_text.delete(1.0, tk.END)
        
        if recommendations:
            self.recommendations_text.insert(tk.END, f"Recommended courses for {student.get_name()}:\n\n")
            for i, course in enumerate(recommendations, 1):
                self.recommendations_text.insert(tk.END, 
                    f"{i}. {course.get_title()} (ID: {course.get_course_id()})\n")
                self.recommendations_text.insert(tk.END,
                    f"   Category: {course.get_category()} | Rating: {course.get_avg_rating():.1f}\n")
                self.recommendations_text.insert(tk.END,
                    f"   Price: ${course.get_price()} | Students: {course.get_enrolled_cou()}\n\n")
        else:
            self.recommendations_text.insert(tk.END, "No recommendations available.")

    def create_dashboard_tab(self):
        frame = ttk.Frame(self.tab_dashboard, padding=20)
        frame.pack(pady=20)
        
        ttk.Label(frame, text="Student ID for Dashboard:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.dashboard_student_entry = ttk.Entry(frame, width=30)
        self.dashboard_student_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Show Dashboard", command=self.show_dashboard).grid(row=1, column=0, columnspan=2, pady=15)
        
        self.dashboard_frame = ttk.Frame(frame)
        self.dashboard_frame.grid(row=2, column=0, columnspan=2, pady=10)

    def show_dashboard(self):
        student_id = self.dashboard_student_entry.get()
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID")
            return
            
        student = self.manager.get_student(student_id)
        if not student:
            messagebox.showerror("Error", "Student not found")
            return
            
        # clear previous widgets
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
            
        # display dashboard
        dashboard_text = tk.Text(self.dashboard_frame, height=10, width=80, font=('Arial', 11))
        dashboard_text.pack(pady=10)
        
        dashboard_text.insert(tk.END, f"=== STUDENT DASHBOARD ===\n\n")
        dashboard_text.insert(tk.END, f"Name: {student.get_name()}\n")
        dashboard_text.insert(tk.END, f"Email: {student.get_email()}\n")
        dashboard_text.insert(tk.END, f"Total Enrolled Courses: {len(student.get_registered_modules())}\n")
        dashboard_text.insert(tk.END, f"Preferences: {', '.join(student.get_preferences())}\n\n")
        
        # show enrolled courses
        if student.get_registered_modules():
            dashboard_text.insert(tk.END, "Enrolled Courses:\n")
            for course_id in student.get_registered_modules():
                course = self.manager.get_course(course_id)
                if course:
                    dashboard_text.insert(tk.END, f"  - {course.get_title()} (Rating: {course.get_avg_rating():.1f})\n")
        else:
            dashboard_text.insert(tk.END, "No enrolled courses.\n")
            
        dashboard_text.configure(state='disabled')

    def create_report_tab(self):
        frame = ttk.Frame(self.tab_reports, padding=20)
        frame.pack(pady=10)
        
        ttk.Button(frame, text="Show Platform Statistics", command=self.show_platform_stats).pack(pady=5)
        ttk.Button(frame, text="Show Recent Enrollments (10 days)", command=self.show_recent_enrollments).pack(pady=5)
        ttk.Button(frame, text="Show Top Rated Courses", command=self.show_top_courses).pack(pady=5)
        
        self.report_text = tk.Text(frame, height=25, width=90, font=('Arial', 11))
        self.report_text.pack(pady=10)

    def show_platform_stats(self):
        stats = self.manager.get_system_view()
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, "=== PLATFORM STATISTICS ===\n\n")
        for k, v in stats.items():
            label = k.replace('_', ' ').title()
            self.report_text.insert(tk.END, f"{label}: {v}\n")
            
    def show_recent_enrollments(self):
        report = self.manager.get_report(10)
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, f"=== RECENT ENROLLMENTS ({report['period']}) ===\n\n")
        self.report_text.insert(tk.END, f"Total Enrollments: {report['total_enrollments']}\n\n")
        
        if report['enrollments']:
            for i, enroll in enumerate(report['enrollments'], 1):
                self.report_text.insert(tk.END, 
                    f"{i}. {enroll['student']} enrolled in {enroll['course']}\n")
                self.report_text.insert(tk.END, f"   Date: {enroll['date'].strftime('%Y-%m-%d %H:%M')}\n\n")
        else:
            self.report_text.insert(tk.END, "No recent enrollments.\n")
            
    def show_top_courses(self):
        board = self.manager.get_board(10)
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, "=== TOP RATED COURSES ===\n\n")
        
        for i, course in enumerate(board, 1):
            self.report_text.insert(tk.END, 
                f"{i}. {course['title']} (ID: {course['course_id']})\n")
            self.report_text.insert(tk.END,
                f"   Rating: {course['average_rating']} | Students: {course['enrolled_students']}\n")
            self.report_text.insert(tk.END,
                f"   Total Ratings: {course['total_ratings']}\n\n")

    def create_admin_tab(self):
        frame = ttk.Frame(self.tab_admin, padding=20)
        frame.pack(pady=20)
        
        ttk.Label(frame, text="Admin Key:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.admin_key_entry = ttk.Entry(frame, width=30, show="*")
        self.admin_key_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Login as Admin", command=self.admin_login).grid(row=1, column=0, columnspan=2, pady=15)
        
        self.admin_frame = ttk.Frame(frame)
        self.admin_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
    def admin_login(self):
        key = self.admin_key_entry.get()
        if self.manager.verify_admin_key(key):
            self.admin_log_in = True
            self.show_admin_controls()
            messagebox.showinfo("Success", "Admin login successful!")
        else:
            messagebox.showerror("Error", "Invalid admin key")
            
    def show_admin_controls(self):
        # clear existing widgets
        for widget in self.admin_frame.winfo_children():
            widget.destroy()
            
        # add admin controls
        ttk.Label(self.admin_frame, text=" admin control ", font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Button(self.admin_frame, text="Generate System Report", 
                  command=self.generate_system_report).pack(pady=5)
        ttk.Button(self.admin_frame, text="Show Course Leaderboard", 
                  command=self.show_course_leaderboard).pack(pady=5)
        ttk.Button(self.admin_frame, text="System Maintenance", 
                  command=self.system_maintenance).pack(pady=5)
        ttk.Button(self.admin_frame, text="Logout", 
                  command=self.admin_logout).pack(pady=20)
                  
    def generate_system_report(self):
        if not self.admin_log_in:
            messagebox.showerror("Error", "Admin access required")
            return
            
        stats = self.manager.get_system_view()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        report = f" system report \nDate: {current_time}\n\n"
        for k, v in stats.items():
            label = k.replace('_', ' ').title()
            report += f"{label}: {v}\n"
            
        with open("system_report.txt", "w") as f:
            f.write(report)
        messagebox.showinfo("Success", "System report generated: system_report.txt")
        
    def show_course_leaderboard(self):
        if not self.admin_log_in:
            messagebox.showerror("Error", "Admin access required")
            return
            
        board = self.manager.get_board(5)
        leaderboard_text = "=== COURSE LEADERBOARD ===\n\n"
        
        for i, course in enumerate(board, 1):
            leaderboard_text += f"{i}. {course['title']} - Rating: {course['average_rating']} ({course['total_ratings']} ratings)\n"
            
        messagebox.showinfo("Course Leaderboard", leaderboard_text)
        
    def system_maintenance(self):
        if not self.admin_log_in:
            messagebox.showerror("Error", "Admin access required")
            return
            
        response = messagebox.askyesno("System Maintenance", 
                                      "Initiate system maintenance? This may temporarily affect performance.")
        if response:
            messagebox.showinfo("Maintenance", "System maintenance initiated. Users may experience brief delays.")
            
    def admin_logout(self):
        self.admin_log_in = False
        self.admin_key_entry.delete(0, tk.END)
        self.show_admin_controls()
        messagebox.showinfo("Logout", "Admin logged out successfully")

    def run(self):
        self.window.mainloop()



manager = Admin()
gui = GUI(manager)
gui.run()