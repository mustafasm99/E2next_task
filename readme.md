# ⚡ FastAPI Restful API

This project is a clean and reusable **FastAPI Project** that provides a solid foundation for building RESTful APIs using a controller-router pattern. It follows best practices for separation of concerns by abstracting database operations and API endpoint definitions into reusable base classes.

---

## ✨ Features

- `BaseController` for generic CRUD operations using SQLModel
- `BaseRouter` for easily setting up REST API routes
- DRY architecture for scalable FastAPI projects
- Type-safe and flexible using Python generics
- Built-in HTTPException handling
- Dependency injection ready (e.g., auth, DB sessions)
- Customizable endpoints and models
- Follows clean code principles and separation of concerns

---

## 📁 Project Structure

```
app/
├── controller/
│   └── base_controller.py
├── endpoints/
│   └── base_router.py
├── models/
│   └── users/
|   |   └── user.py
|   └── task
|       └── task_model.py
├── db/
│   └── depend.py
├── core/
│     └── settings.py
main.py
```

---

## 📃 API Docs

1. Auth Collections
   | Method | Path | Description |
   | ------ | --------------- | ------------------------------------------ |
   | POST | `auth/login` | Login the user with user name and password |
   | POST | `auth/register` | Create new user |
   | Get | `auth/profile` | Get the current user by the token |

2. Task Collections
   | Method | Path | Description |
   | ------ | --------------- | ------------------------------------------ |
   | GET | `tasks/analytics` | Get the total count of the tasks and the number of completed and pending tasks |
   | GET | `tasks/search` | Search for task by its title |
   | GET | `tasks` | Get all my tasks & filter tasks base on there status |
   | POST | `tasks` | Create new Task |
   | PUT | `tasks\{id}` | Update task by its id |
   | DELETE | `tasks\{id}` | Delete the task by its id |

---

## 📦 Installation

1. Clone the repo

```bash
git clone https://github.com/mustafasm99/E2next_task.git
cd E2next_task
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Run The App

1. make sure you are inside the backend folder
2. use `uvicorn app.main:app --reload`
3. go to `127.0.0.1:8000/docs` to see the swagger docs

---

## 🚀 Usage

### Example: Create a new controller and router for a model

1. Define your model in `app/models/your_model.py`:

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
```

2. Create a controller and router:

```python
from app.controller.base_controller import BaseController
from app.router.base_router import BaseRouter
from app.models.your_model import Item

item_controller = BaseController(Item)

item_router = BaseRouter(
    tag=["Items"],
    controller=item_controller,
    model=Item,
    create_type=Item,
    prefix="/items",
)
```

3. Include the router in `main.py`:

```python
from fastapi import FastAPI
from app.routes.item_router import item_router  # adjust import path

app = FastAPI()
app.include_router(item_router.router)
```

---

## 📚 How It Works

### ✅ BaseController

Provides generic methods for:

- `get(id)`
- `read()`
- `create(data)`
- `update(id, data)`
- `delete(id)`

All methods are asynchronous and interact with the database using SQLModel.

### ✅ BaseRouter

Automatically registers CRUD endpoints:

| Method | Path    | Description       |
| ------ | ------- | ----------------- |
| GET    | ``      | Get all items     |
| GET    | `/{id}` | Get item by ID    |
| POST   | ``      | Create new item   |
| PUT    | `/{id}` | Update item by ID |
| DELETE | `/{id}` | Delete item by ID |

---

## 🛡️ Authentication Support

You can pass a `User` or other dependency object through `auth_object` to secure routes:

```python
BaseRouter(..., auth_object=Depends(get_current_user))
```

---

## 🧪 Testing

You can easily write tests for your controller or router by mocking the session or using test databases.

---

## 📖 Requirements

- Python 3.10+
- FastAPI
- SQLModel
- Uvicorn
- (Optional) Alembic for migrations

Install with:

```bash
pip install fastapi uvicorn sqlmodel
```

---

## 🤝 Contributing

Pull requests are welcome. Feel free to open issues or suggest improvements.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Mustafa Saad**  
GitHub: [@yourusername](https://github.com/mustafasm99)  
LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/mustafa-saad-5b154b109/)
