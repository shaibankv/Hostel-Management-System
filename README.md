# Hostel Management System

A Django-based web application for managing hostel operations including students, rooms, fees, employees, visitor logs, attendance presence, and complaints.

---

## Tech Stack

- **Framework:** Django (Python)
- **Database:** SQLite3 (`db.sqlite3`)
- **Auth:** Custom User Model extending `AbstractUser`
- **Media Storage:** Local filesystem (`media/`)
- **Virtual Env:** `hmsvenv/`

---

## Project Directory Structure

```
Hostel Management System/
└── HostelManagementSystem/               ← Django project root
    ├── manage.py
    ├── db.sqlite3
    ├── media/
    │   ├── fee_receipt/                  ← Uploaded fee receipts (PDF)
    │   ├── id_proof/                     ← Student ID proof uploads (PDF)
    │   └── students_photo/               ← Student profile photos (JPG)
    │
    ├── HostelManagementSystem/           ← Django project config package
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py                       ← Root URL conf
    │   ├── asgi.py
    │   └── wsgi.py
    │
    ├── accounts/                         ← Authentication & role management app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   ├── migrations/
    │   └── templates/
    │       ├── login.html
    │       ├── admin_dashboard.html
    │       ├── warden_dashboard.html
    │       ├── staff_dashboard.html
    │       └── student_dashboard.html
    │
    ├── student/                          ← Student management app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   ├── migrations/
    │   └── templates/
    │       ├── student_list.html
    │       ├── add_student.html
    │       ├── edit_student.html
    │       ├── delete_student.html
    │       └── update_profile.html
    │
    ├── room/                             ← Room management app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   ├── migrations/
    │   └── templates/
    │       ├── room_list.html
    │       ├── add_room.html
    │       ├── edit_room.html
    │       └── delete_room.html
    │
    ├── fee/                              ← Fee management app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   ├── migrations/
    │   └── templates/
    │       ├── fee_list.html
    │       ├── add_fee.html
    │       └── student_fee.html
    │
    ├── employee/                         ← Employee management app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   ├── migrations/
    │   └── templates/
    │       ├── employee_list.html
    │       ├── add_employee.html
    │       ├── edit_employee.html
    │       └── delete_employee.html
    │
    ├── presence/                         ← Student presence/attendance app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   ├── migrations/
    │   └── templates/                    ← (templates directory present, no HTML files yet)
    │
    ├── complaints/                       ← Complaint management app
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   ├── migrations/
    │   └── templates/
    │       ├── list_complaints.html
    │       └── add_complaint.html
    │
    └── visitor/                          ← Visitor log management app
        ├── models.py
        ├── views.py
        ├── urls.py
        ├── admin.py
        ├── apps.py
        ├── tests.py
        ├── migrations/
        └── templates/
            ├── list_visitors.html
            └── add_visitor.html
```

---

## Apps & Modules

### `accounts` — Authentication & Role-Based Access

**Model: `UserList`** (extends `AbstractUser`)

| Field  | Type        | Notes                                      |
|--------|-------------|--------------------------------------------|
| role   | CharField   | Choices: `Admin`, `Warden`, `Staff`, `Student` |
| + all Django AbstractUser fields (username, password, email, etc.) |

**URLs:**

| URL Pattern       | View           | Name        |
|-------------------|----------------|-------------|
| `/`               | `login_view`   | `login`     |
| `/dashboard/`     | `dashboard_view` | `dashboard` |
| `/logout/`        | `logout_view`  | `logout`    |

**Templates:**
- `login.html` — Login form
- `admin_dashboard.html` — Admin home
- `warden_dashboard.html` — Warden home
- `staff_dashboard.html` — Staff home
- `student_dashboard.html` — Student home

---

### `student` — Student Management

**Model: `Student`**

| Field           | Type          | Notes                                    |
|-----------------|---------------|------------------------------------------|
| user            | OneToOneField | → `accounts.UserList`, CASCADE           |
| name            | CharField     | max_length=30                            |
| reg_number      | CharField     | max_length=25, unique                    |
| dob             | DateField     | "Date of Birth"                          |
| course          | CharField     | max_length=20                            |
| year            | IntegerField  |                                          |
| phone           | CharField     | max_length=13, default='+91'             |
| email           | EmailField    |                                          |
| home_address    | TextField     |                                          |
| guardian_name   | CharField     | max_length=30                            |
| guardian_phone  | CharField     | max_length=13, default='+91'             |
| guardian_email  | EmailField    |                                          |
| room            | ForeignKey    | → `room.Room`, SET_NULL, nullable        |
| photo           | ImageField    | upload_to='students_photo/'              |
| id_proof        | FileField     | upload_to='id_proof/'                    |

> Room capacity is enforced via `clean()` — raises `ValidationError` if room is full.

**URLs:**

| URL Pattern                    | View             | Name             |
|--------------------------------|------------------|------------------|
| `/student_list/`               | `student_list`   | `student_list`   |
| `/add_student/`                | `add_student`    | `add_student`    |
| `/edit_student/<int:id>/`      | `edit_student`   | `edit_student`   |
| `/update_profile/`             | `update_profile` | `update_profile` |
| `/delete_student/<int:id>/`    | `delete_student` | `delete_student` |

**Templates:**
- `student_list.html` — All students table
- `add_student.html` — Registration form (with file upload)
- `edit_student.html` — Edit form (admin/warden)
- `delete_student.html` — Confirm delete
- `update_profile.html` — Student self-update

---

### `room` — Room Management

**Model: `Room`**

| Field    | Type      | Notes                          |
|----------|-----------|--------------------------------|
| block    | CharField | max_length=5                   |
| room_no  | CharField | max_length=10                  |
| capacity | IntegerField |                              |

> `unique_together = ['block', 'room_no']`

**URLs:**

| URL Pattern                 | View          | Name          |
|-----------------------------|---------------|---------------|
| `/room_list/`               | `room_list`   | `room_list`   |
| `/add_room/`                | `add_room`    | `add_room`    |
| `/edit_room/<int:id>/`      | `edit_room`   | `edit_room`   |
| `/delete_room/<int:id>/`    | `delete_room` | `delete_room` |

**Templates:**
- `room_list.html` — All rooms
- `add_room.html` — Add room form
- `edit_room.html` — Edit room form
- `delete_room.html` — Confirm delete

---

### `fee` — Fee Management

**Model: `Fee`**

| Field          | Type          | Notes                                  |
|----------------|---------------|----------------------------------------|
| student        | ForeignKey    | → `student.Student`, CASCADE           |
| amount         | DecimalField  | max_digits=10, decimal_places=2        |
| academic_year  | CharField     | max_length=20                          |
| payment_date   | DateField     |                                        |
| due_date       | DateField     |                                        |
| status         | CharField     | default="Pending"                      |
| payment_method | CharField     | max_length=30                          |
| transaction_id | CharField     | max_length=40                          |
| receipt        | FileField     | upload_to='fee_receipt/'               |

**URLs:**

| URL Pattern                  | View           | Name           |
|------------------------------|----------------|----------------|
| `/add_fee/<int:id>/`         | `add_fee`      | `add_fee`      |
| `/fee_list/`                 | `fee_list`     | `fee_list`     |
| `/student_fee/<int:id>/`     | `student_fee`  | `student_fee`  |

**Templates:**
- `fee_list.html` — All fee records
- `add_fee.html` — Add fee entry (with receipt upload)
- `student_fee.html` — Individual student fee view

---

### `employee` — Employee/Staff Management

**Model: `Employee`**

| Field   | Type          | Notes                         |
|---------|---------------|-------------------------------|
| name    | CharField     | max_length=30                 |
| role    | CharField     | max_length=20                 |
| phone   | CharField     | max_length=14, default='+91'  |
| email   | EmailField    |                               |
| salary  | DecimalField  | max_digits=10, decimal_places=2 |
| shift   | CharField     | max_length=25                 |

**URLs:**

| URL Pattern                    | View              | Name              |
|--------------------------------|-------------------|-------------------|
| `/employee_list/`              | `employee_list`   | `employee_list`   |
| `/add_employee/`               | `add_employee`    | `add_employee`    |
| `/edit_employee/<int:id>/`     | `edit_employee`   | `edit_employee`   |
| `/delete_employee/<int:id>/`   | `delete_employee` | `delete_employee` |

**Templates:**
- `employee_list.html` — All employees table
- `add_employee.html` — Add form
- `edit_employee.html` — Edit form
- `delete_employee.html` — Confirm delete

---

### `presence` — Student Presence / In-Out Log

**Model: `Presence`**

| Field     | Type       | Notes                            |
|-----------|------------|----------------------------------|
| student   | ForeignKey | → `student.Student`, CASCADE     |
| date_out  | DateField  |                                  |
| time_out  | TimeField  |                                  |
| date_in   | DateField  | null, blank                      |
| time_in   | TimeField  | null, blank                      |
| status    | CharField  | max_length=10 (e.g. Out/In)      |
| reason    | TextField  |                                  |

**URLs:**

| URL Pattern                 | View             | Name             |
|-----------------------------|------------------|------------------|
| `/mark_out/<int:id>/`       | `mark_out`       | `mark_out`       |
| `/mark_in/<int:id>/`        | `mark_in`        | `mark_in`        |
| `/presence_list/`           | `presence_list`  | `presence_list`  |

**Templates:**
- ⚠️ No HTML templates created yet — `templates/` directory exists but is empty.

---

### `complaints` — Complaint Management

**Model: `Complaints`**

| Field       | Type      | Notes          |
|-------------|-----------|----------------|
| name        | CharField | max_length=30  |
| block       | CharField | max_length=5   |
| room_no     | CharField | max_length=10  |
| complaint   | CharField | max_length=40  |
| description | TextField |                |

**URLs:**

| URL Pattern          | View               | Name               |
|----------------------|--------------------|--------------------|
| `/list_complaints/`  | `list_complaints`  | `list_complaints`  |
| `/add_complaint/`    | `add_complaint`    | `add_complaint`    |

**Templates:**
- `list_complaints.html` — All complaints
- `add_complaint.html` — Submit complaint form

---

### `visitor` — Visitor Log

**Model: `Visitor`**

| Field         | Type       | Notes                        |
|---------------|------------|------------------------------|
| student       | ForeignKey | → `student.Student`, CASCADE |
| visitor_name  | CharField  | max_length=30                |
| visit_date    | DateField  |                              |
| visit_time    | TimeField  |                              |
| visit_reason  | TextField  |                              |

**URLs:**

| URL Pattern                    | View             | Name             |
|--------------------------------|------------------|------------------|
| `/list_visitors/`              | `list_visitors`  | `list_visitors`  |
| `/add_visitor/<int:id>/`       | `add_visitor`    | `add_visitor`    |

**Templates:**
- `list_visitors.html` — All visitor records
- `add_visitor.html` — Log a new visitor

---

## Root URL Configuration

Defined in `HostelManagementSystem/urls.py`:

| Include Path     | App Module          |
|------------------|---------------------|
| `/`              | `accounts.urls`     |
| `/student/`      | `student.urls`      |
| `/room/`         | `room.urls`         |
| `/fee/`          | `fee.urls`          |
| `/employee/`     | `employee.urls`     |
| `/presence/`     | `presence.urls`     |
| `/complaints/`   | `complaints.urls`   |
| `/visitor/`      | `visitor.urls`      |
| `/admin/`        | Django Admin        |

---

## Settings Summary (`settings.py`)

| Setting             | Value                         |
|---------------------|-------------------------------|
| `AUTH_USER_MODEL`   | `accounts.UserList`           |
| `LOGIN_URL`         | `"login"`                     |
| `LOGIN_REDIRECT_URL`| `"dashboard"`                 |
| `MEDIA_URL`         | `/media/`                     |
| `MEDIA_ROOT`        | `media/`                      |
| `DATABASES`         | SQLite3 (`db.sqlite3`)        |
| `INSTALLED_APPS`    | accounts, student, room, employee, fee, presence, complaints, visitor |

---

## Role-Based Access Summary

| Role    | Typical Permissions                                              |
|---------|------------------------------------------------------------------|
| Admin   | Full access — all apps, dashboards, CRUD                        |
| Warden  | Student, room, presence, complaints, visitor management         |
| Staff   | Employee and presence logs                                      |
| Student | View own profile, fee, update profile, add complaint            |

---

## Media Upload Paths

| Upload Type     | Field         | Path                  |
|-----------------|---------------|-----------------------|
| Student photos  | `photo`       | `media/students_photo/` |
| ID proof docs   | `id_proof`    | `media/id_proof/`     |
| Fee receipts    | `receipt`     | `media/fee_receipt/`  |

---

## Known Gaps / TODO

- `presence/templates/` — No HTML templates created yet. Needs: `presence_list.html`, `mark_out.html`, `mark_in.html`
- All templates are currently empty stubs (very small file sizes indicate placeholder content)
- No base/layout template detected — a shared `base.html` with navigation should be created
- No `forms.py` files — forms appear to be handled directly in views
- No `requirements.txt` — should be generated from venv for reproducibility

---

## Quick Start

```bash
# Activate virtual environment
source hmsvenv/Scripts/activate       # Windows
# source hmsvenv/bin/activate         # Linux/Mac

cd HostelManagementSystem

# Apply migrations
python manage.py migrate

# Create superuser (Admin role)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## Model Relationship Diagram

```
UserList (accounts)
    │
    └── Student (1:1)
            │
            ├── Room (FK) ←── Room (room)
            │
            ├── Fee (FK) ←── Fee (fee)
            │
            ├── Presence (FK) ←── Presence (presence)
            │
            └── Visitor (FK) ←── Visitor (visitor)

Employee (employee)     ← standalone, no FK relations
Complaints (complaints) ← standalone, no FK relations
```
