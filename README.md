 Student Grade Management System

2A student grade management system built using **Clean Architecture** principles. The main goal is to separate business logic from technical details (database, interfaces, framework), making the system easier to test, maintain, and adapt.

---

What is Clean Architecture

Clean Architecture is a software design principle stating that an application's core business logic should be independent of, and isolated from, external technical details such as the user interface, database, and frameworks.

This is achieved by organizing code into concentric layers, where **dependencies always point inward**: outer layers may depend on inner layers (business rules), but never the reverse.

The goal is to produce systems that are easier to:
- **Test** — business logic can be tested without a database or framework
- **Maintain** — changes in one layer don't affect other layers
- **Adapt** — technology changes (e.g. switching SQLite for PostgreSQL) don't affect business logic

---

Advantages of this project

- Reduces human error in grade calculation
- Gives students and staff faster access to accurate records
- Makes it easier for the institution to track academic performance over time

---

 Project structure

```
student_grade_management/
│8
├── entities/                 # Business rules, technology-independent
│   ├── student.py
│   ├── course.py
│   └── grade.py
│
├── use_cases/                 # Application logic (what the system does)
│   ├── add_grade.py
│   ├── calculate_average.py
│2   └── list_student_grades.py
│
├── interfaces/                 # Contracts/abstractions between layers
│   ├── repositories/
│   │   ├── student_repository.py
│   │   ├── course_repository.py
│   │   └── grade_repository.py
│   └── presenters/
│       └── grade_presenter.py
│
├── infrastructure/             # Technical details (database, connection)
│   ├── database/
│   │   ├── models.py
│   │   └── connection.py
│   └── repositories/
│       ├── student_repository_impl.py
│       ├── course_repository_impl.py
│       └── grade_repository_impl.py
│
├── adapters/                   # Bridge between the outside world (API/web) and use cases
│   ├── controllers/
│   │   └── grade_controller.py
│   └── api/
│       └── routes.py
│
├── tests/
│   ├── test_entities/
│   ├── test_use_cases/
│   └── test_infrastructure/
8│
├── main.py
├── requirements.txt
└── README.md
```

Layer descriptions

| Layer | Responsibility |
|---|---|
| **entities** | Core business objects and rules (Student, Course, Grade) — no external dependencies |
| **use_cases** | Actions the application can perform (add a grade, calculate average, list grades) |
| **interfaces** | Abstract contracts (repository, presenter) defining WHAT must be done, not HOW |
| **infrastructure** | Concrete implementations: database connection, data models, actual repositories |
| **adapters** | Controllers and API routes that receive external requests and call the use cases |

Dependency direction: `adapters → infrastructure → interfaces → use_cases → entities`
(outer layers depend on inner layers, never the reverse)

---

 Prerequisites

- Python 3.10+
- pip
- Django 5.x



Installation

```bash
git clone <repo-url>
cd student_grade_management
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

---

 Configuration

Check/update the database settings in Django's `settings.py` (DATABASES), along with `infrastructure/database/connection.py` if you're pointing the infrastructure layer to the same database.

---

Running the application

```bash
python manage.py runserver
```

`main.py` can remain as an entry-point script to run use cases directly (without the web server), useful for testing or demos.



 Usage example

Use cases are independent of Django — they can be called from a view, a controller, or a script:

```python
from use_cases.add_grade import AddGrade
from use_cases.calculate_average import CalculateAverage

 Add a grade for a student
add_grade = AddGrade(grade_repository)
add_grade.execute(student_id=1, course_id=2, score=85)

 Calculate a student's average
calculate_average = CalculateAverage(grade_repository)
average = calculate_average.execute(student_id=1)
```



 Tests

```bash
pytest tests/


 Technology used

**Language**: Python
- **Framework**: Django
- **Database**: SQLite by default (can easily be swapped for PostgreSQL/MySQL thanks to the layer separation)
- **API**: Django views / Django REST Framework (in `adapters/api/routes.py` and `adapters/controllers/`)


Contributing

Pull requests are welcome. Please follow the layer structure and keep interfaces independent from concrete implementations.


