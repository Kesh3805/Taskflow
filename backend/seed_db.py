"""
Seed script for TaskFlow database
Populates the database with sample data for testing
"""
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.project import Project, ProjectMember
from app.models.task import Task
from app.models.comment import Comment
from app.models.label import Label
from app.models.activity_log import ActivityLog

def seed_database():
    app = create_app()
    with app.app_context():
        print("🌱 Seeding database with sample data...\n")
        
        # Drop and recreate all tables
        print("Recreating database tables with new schema...")
        db.drop_all()
        db.create_all()
        print("   ✓ Tables recreated successfully\n")
        
        # Create users
        print("👥 Creating users...")
        admin = User(name="Admin User", email="admin@taskflow.com", role="ADMIN")
        admin.set_password("admin123")
        
        alice = User(name="Alice Johnson", email="alice@taskflow.com", role="MEMBER")
        alice.set_password("alice123")
        
        bob = User(name="Bob Smith", email="bob@taskflow.com", role="MEMBER")
        bob.set_password("bob123")
        
        charlie = User(name="Charlie Davis", email="charlie@taskflow.com", role="MEMBER")
        charlie.set_password("charlie123")
        
        db.session.add_all([admin, alice, bob, charlie])
        db.session.commit()
        print(f"   ✓ Created {User.query.count()} users")
        
        # Create projects
        print("\n📁 Creating projects...")
        project1 = Project(
            name="Website Redesign",
            description="Modernize company website with new design and features",
            owner_id=admin.id
        )
        db.session.add(project1)
        db.session.flush()
        
        # Add members with roles for project1
        # Admin is owner and PM
        ProjectMember(user_id=admin.id, project_id=project1.id, role="PM")
        # Alice is also a PM (project manager)
        db.session.add(ProjectMember(user_id=alice.id, project_id=project1.id, role="PM"))
        # Bob is regular member
        db.session.add(ProjectMember(user_id=bob.id, project_id=project1.id, role="MEMBER"))
        
        project2 = Project(
            name="Mobile App Development",
            description="Build native mobile app for iOS and Android",
            owner_id=alice.id
        )
        db.session.add(project2)
        db.session.flush()
        
        # Add members with roles for project2
        # Alice is owner and PM
        db.session.add(ProjectMember(user_id=alice.id, project_id=project2.id, role="PM"))
        # Bob is also a PM
        db.session.add(ProjectMember(user_id=bob.id, project_id=project2.id, role="PM"))
        # Charlie is regular member
        db.session.add(ProjectMember(user_id=charlie.id, project_id=project2.id, role="MEMBER"))
        
        project3 = Project(
            name="Marketing Campaign Q1",
            description="Launch social media and email marketing campaign",
            owner_id=bob.id
        )
        db.session.add(project3)
        db.session.flush()
        
        # Add members with roles for project3
        # Bob is owner and PM
        db.session.add(ProjectMember(user_id=bob.id, project_id=project3.id, role="PM"))
        # Charlie is regular member
        db.session.add(ProjectMember(user_id=charlie.id, project_id=project3.id, role="MEMBER"))
        # Admin is regular member (showing admins can also be members)
        db.session.add(ProjectMember(user_id=admin.id, project_id=project3.id, role="MEMBER"))
        
        db.session.add_all([project1, project2, project3])
        db.session.commit()
        print(f"   ✓ Created {Project.query.count()} projects")
        
        # Create tasks for Website Redesign
        print("\n✅ Creating tasks...")
        tasks_p1 = [
            Task(
                title="Design new homepage mockup",
                description="Create modern, responsive homepage design in Figma",
                status="DONE",
                priority="HIGH",
                project_id=project1.id,
                assigned_to=alice.id,
                due_date=(datetime.now() - timedelta(days=5)).date()
            ),
            Task(
                title="Implement responsive navigation",
                description="Build mobile-friendly navigation menu with hamburger icon",
                status="DONE",
                priority="HIGH",
                project_id=project1.id,
                assigned_to=bob.id,
                due_date=(datetime.now() - timedelta(days=2)).date()
            ),
            Task(
                title="Develop contact form",
                description="Create contact form with validation and email integration",
                status="IN_PROGRESS",
                priority="MEDIUM",
                project_id=project1.id,
                assigned_to=alice.id,
                due_date=(datetime.now() + timedelta(days=3)).date()
            ),
            Task(
                title="Optimize images for web",
                description="Compress and optimize all images for faster loading",
                status="TODO",
                priority="MEDIUM",
                project_id=project1.id,
                assigned_to=bob.id,
                due_date=(datetime.now() + timedelta(days=5)).date()
            ),
            Task(
                title="SEO optimization",
                description="Implement meta tags, structured data, and SEO best practices",
                status="TODO",
                priority="LOW",
                project_id=project1.id,
                assigned_to=None,
                due_date=(datetime.now() + timedelta(days=10)).date()
            ),
        ]
        
        # Create tasks for Mobile App
        tasks_p2 = [
            Task(
                title="Setup React Native project",
                description="Initialize React Native project with required dependencies",
                status="DONE",
                priority="HIGH",
                project_id=project2.id,
                assigned_to=bob.id,
                due_date=(datetime.now() - timedelta(days=7)).date()
            ),
            Task(
                title="Design app navigation flow",
                description="Create navigation structure and screen flow diagrams",
                status="DONE",
                priority="HIGH",
                project_id=project2.id,
                assigned_to=alice.id,
                due_date=(datetime.now() - timedelta(days=4)).date()
            ),
            Task(
                title="Implement user authentication",
                description="Build login/register screens with JWT authentication",
                status="IN_PROGRESS",
                priority="HIGH",
                project_id=project2.id,
                assigned_to=charlie.id,
                due_date=(datetime.now() + timedelta(days=2)).date()
            ),
            Task(
                title="Create home screen UI",
                description="Design and implement main dashboard screen",
                status="IN_PROGRESS",
                priority="MEDIUM",
                project_id=project2.id,
                assigned_to=alice.id,
                due_date=(datetime.now() + timedelta(days=4)).date()
            ),
            Task(
                title="Setup push notifications",
                description="Integrate Firebase Cloud Messaging for push notifications",
                status="TODO",
                priority="MEDIUM",
                project_id=project2.id,
                assigned_to=bob.id,
                due_date=(datetime.now() + timedelta(days=8)).date()
            ),
            Task(
                title="Write unit tests",
                description="Create comprehensive unit test suite for core functionality",
                status="TODO",
                priority="LOW",
                project_id=project2.id,
                assigned_to=None,
                due_date=(datetime.now() + timedelta(days=15)).date()
            ),
        ]
        
        # Create tasks for Marketing Campaign
        tasks_p3 = [
            Task(
                title="Define target audience",
                description="Research and document target customer personas",
                status="DONE",
                priority="HIGH",
                project_id=project3.id,
                assigned_to=bob.id,
                due_date=(datetime.now() - timedelta(days=10)).date()
            ),
            Task(
                title="Create social media content calendar",
                description="Plan 30 days of social media posts across platforms",
                status="IN_PROGRESS",
                priority="HIGH",
                project_id=project3.id,
                assigned_to=charlie.id,
                due_date=(datetime.now() + timedelta(days=1)).date()
            ),
            Task(
                title="Design email templates",
                description="Create responsive email templates for campaign",
                status="IN_PROGRESS",
                priority="MEDIUM",
                project_id=project3.id,
                assigned_to=admin.id,
                due_date=(datetime.now() + timedelta(days=3)).date()
            ),
            Task(
                title="Setup Google Analytics tracking",
                description="Configure GA4 events and conversion tracking",
                status="TODO",
                priority="MEDIUM",
                project_id=project3.id,
                assigned_to=charlie.id,
                due_date=(datetime.now() + timedelta(days=5)).date()
            ),
            Task(
                title="Launch Instagram ads campaign",
                description="Create and launch targeted Instagram ad campaign",
                status="TODO",
                priority="HIGH",
                project_id=project3.id,
                assigned_to=None,
                due_date=(datetime.now() + timedelta(days=7)).date()
            ),
        ]
        
        all_tasks = tasks_p1 + tasks_p2 + tasks_p3
        db.session.add_all(all_tasks)
        db.session.commit()
        print(f"   ✓ Created {Task.query.count()} tasks")
        
        # Print summary
        print("\n" + "="*60)
        print("✅ Database seeding completed successfully!\n")
        print("📊 Summary:")
        print(f"   Users:    {User.query.count()}")
        print(f"   Projects: {Project.query.count()}")
        print(f"   Tasks:    {Task.query.count()}")
        print("\n🔐 Test Accounts:")
        print("   Admin:   admin@taskflow.com / admin123")
        print("   Alice:   alice@taskflow.com / alice123")
        print("   Bob:     bob@taskflow.com / bob123")
        print("   Charlie: charlie@taskflow.com / charlie123")
        print("="*60)

if __name__ == "__main__":
    seed_database()
