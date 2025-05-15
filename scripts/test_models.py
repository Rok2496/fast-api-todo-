from app.db.database import SessionLocal, engine
from app.db import models
from app.core import auth
import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

# Create a database session
db = SessionLocal()

def test_create_user():
    print("Creating test user...")
    # Check if test user already exists
    test_user = db.query(models.User).filter(models.User.email == "test@example.com").first()
    
    if test_user:
        print(f"Test user already exists with ID: {test_user.id}")
        return test_user
    
    # Create a new test user
    hashed_password = auth.get_password_hash("password123")
    new_user = models.User(
        email="test@example.com",
        hashed_password=hashed_password,
        is_active=True,
        is_verified=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"Created new test user with ID: {new_user.id}")
    return new_user

def test_create_todo(user):
    print("\nCreating test todo item...")
    # Create a todo for the test user
    new_todo = models.Todo(
        title="Test Todo Item",
        description="This is a test todo item created for model testing",
        due_date=datetime.datetime.utcnow() + datetime.timedelta(days=1),
        completed=False,
        owner_id=user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    print(f"Created new todo with ID: {new_todo.id}")
    return new_todo

def test_retrieve_todos(user):
    print("\nRetrieving todos for user...")
    todos = db.query(models.Todo).filter(models.Todo.owner_id == user.id).all()
    print(f"Found {len(todos)} todos for user {user.email}:")
    
    for i, todo in enumerate(todos, 1):
        print(f"{i}. {todo.title} - Due: {todo.due_date} - Completed: {todo.completed}")

# Run the tests
try:
    user = test_create_user()
    todo = test_create_todo(user)
    test_retrieve_todos(user)
    print("\nModel tests completed successfully!")
finally:
    db.close() 