import random
import string
from datetime import datetime
import gradio as gr


# ===================== Student =====================
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

    def register_module(self, course_id):
        if course_id not in self.__registered_modules:
            self.__registered_modules.append(course_id)
            self.__registered_date[course_id] = datetime.now()
            return True
        return False


# ===================== Course =====================
class Course:
    def __init__(self, title, description, instructor_id, category, price=0.0):
        self.__course_id = self.gen_course_id()
        self.__title = title
        self.__description = description
        self.__instructor_id = instructor_id
        self.__category = category
        self.__price = price
        self.__ratings = []
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

    def get_creation_date(self):
        return self.__create_date

    def register_student(self, student_id):
        if student_id not in self.__enrolled_students:
            self.__enrolled_students.append(student_id)
            return True
        return False

    def get_enrolled_count(self):
        return len(self.__enrolled_students)


# ===================== Recommendation (optional) =====================
class Recommendation:
    def preferences_score(self, course, student):
        return 50 if course.get_category() in student.get_preferences() else 0

    def popularity_score(self, course):
        return min(course.get_enrolled_count() / 10, 1.5) * 10

    def last_score(self, course):
        return 10 if (datetime.now() - course.get_creation_date()).days < 30 else 0

    def generate(self, courses, student):
        enrolled = student.get_registered_modules()
        scored = []

        for course in courses:
            if course.get_course_id() not in enrolled:
                score = (
                    self.preferences_score(course, student)
                    + self.popularity_score(course)
                    + self.last_score(course)
                )
                scored.append((course, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [c[0].get_title() for c in scored[:5]]


# ===================== Admin =====================
class Admin:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def register_student(self, name, email):
        s = Student(name, email)
        self.students[s.get_student_id()] = s
        return s.get_student_id()

    def add_course(self, title, desc, inst_id, cat, price):
        try:
            price = float(price) if price is not None else 0.0
        except:
            price = 0.0

        c = Course(title, desc, inst_id, cat, price)
        self.courses[c.get_course_id()] = c
        return c.get_course_id()

    def enroll(self, student_id, course_id):
        if student_id not in self.students:
            return "Student not found"

        if course_id not in self.courses:
            return "Course not found"

        s = self.students[student_id]
        c = self.courses[course_id]

        ok1 = s.register_module(course_id)
        ok2 = c.register_student(student_id)

        if ok1 and ok2:
            return "Enrollment successful"
        return "Already enrolled"

    def get_courses(self):
        return [
            f"{cid} - {c.get_title()}"
            for cid, c in self.courses.items()
        ]


admin = Admin()


# ===================== UI Functions =====================
def register_ui(name, email):
    return admin.register_student(name, email)


def add_course_ui(title, desc, inst, cat, price):
    return admin.add_course(title, desc, inst, cat, price)


def enroll_ui(student_id, course_id):
    return admin.enroll(student_id, course_id)


def list_courses_ui():
    return "\n".join(admin.get_courses())


# ===================== Gradio UI =====================
with gr.Blocks() as demo:
    gr.Markdown("# 🎓 Student Management System")

    # ===== ===== Register Student ===== =====
    with gr.Tab("Register Student"):
        name = gr.Textbox(label="Name")
        email = gr.Textbox(label="Email")
        out1 = gr.Textbox(label="Student ID")
        gr.Button("Register").click(register_ui, [name, email], out1)

    # ===== ===== Add Course ===== =====
    with gr.Tab("Add Course"):
        title = gr.Textbox(label="Title")
        desc = gr.Textbox(label="Description")
        inst = gr.Textbox(label="Instructor ID")
        cat = gr.Dropdown(["IT", "Math", "Art"], label="Category")
        price = gr.Number(label="Price")
        out2 = gr.Textbox(label="Course ID")

        gr.Button("Add Course").click(
            add_course_ui, [title, desc, inst, cat, price], out2
        )

    # ===== ===== Enroll Student ===== =====
    with gr.Tab("Enroll Student"):
        sid = gr.Textbox(label="Student ID")
        cid = gr.Textbox(label="Course ID")
        out3 = gr.Textbox(label="Status")

        gr.Button("Enroll").click(enroll_ui, [sid, cid], out3)

    # ===== ===== Course List ===== =====
    with gr.Tab("Courses"):
        course_list = gr.Textbox(label="All Courses", lines=10)
        gr.Button("Refresh").click(list_courses_ui, None, course_list)


demo.launch()