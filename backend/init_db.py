"""
Database initialization script for TaskFlow
Creates all database tables based on SQLAlchemy models
"""
from app import create_app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        from app.extensions import db
        print("Creating database tables...")
        db.create_all()
        print("✓ All tables created successfully!")
        
        # Show created tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\nCreated {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
