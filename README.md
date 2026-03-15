# course_registration_system

A **University Course Registration System** that follows **Domain-Driven Design (DDD)** principles.

---

## Overview

This project is structured to reflect DDD concepts such as:

- **Domain layer**: Business logic and domain models (entities, value objects, domain services).
- **Infrastructure layer**: Technical details like database persistence and repositories.

---

## Project Structure

```
main.py
requirements.txt

/domain
    __init__.py
    models.py          # Domain entities and value objects
    services.py        # Domain services and business logic

/infrastructure
    __init__.py
    database.py        # Persistence setup (e.g., ORM, DB connection)
    repositories.py    # Repository interfaces + implementations
```

---

## How DDD Principles Are Applied

### 1) Domain Model First (Core of the System)
The `domain` package contains the core business concepts:

- **Entities**: Objects with an identity that persists over time (e.g., `Student`, `Course`, `Registration`).
- **Value Objects**: Immutable objects that represent a descriptive aspect of the domain (e.g., `CourseCode`, `Email`, `Schedule`).
- **Domain Services**: Operations that span multiple entities or don’t naturally belong to a single entity (e.g., registration rules or checks).

These classes contain the rules and invariants that govern how the system behaves.

### 2) Separation of Concerns (Layers)
The system is divided into clear layers:

- **Domain**: Business logic and rules (pure Python code, independent of frameworks).
- **Infrastructure**: Technical details such as database access, external APIs, and repositories.

This separation makes it easier to test business rules without needing a database, and to replace infrastructure details without changing the domain logic.

### 3) Repository Pattern (Persistence Decoupling)
The repository pattern abstracts persistence details behind a clean interface. The `infrastructure/repositories.py` module is responsible for:

- Providing methods such as `add_student`, `get_course`, `save_registration`, etc.
- Keeping the domain model independent of how data is stored.

This allows the domain layer to work with domain objects without knowing if they came from an in-memory store, a relational database, or another persistence mechanism.

### 4) Ubiquitous Language
The code is written using terminology that matches the problem domain (courses, students, registrations). This makes the intent of the code clearer and aligns it with the language a domain expert would use.

---

## Why this organization is useful

- **Testability**: Business rules can be tested without touching the database.
- **Maintainability**: Clear separation of concerns makes the code easier to understand and evolve.
- **Flexibility**: You can swap persistence mechanisms or add new UI layers without changing domain logic.

