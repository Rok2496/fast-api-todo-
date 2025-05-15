from app.db.database import engine
from app.db import models

print("Creating database tables...")
models.Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
print("\nYour database is now fully configured and ready to use.")
print("You can start the API with: uvicorn app.main:app --reload") 