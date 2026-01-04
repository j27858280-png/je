#!/usr/bin/env python3
"""
Script to create default admin user for Worker Management System
Run this in Render shell if needed
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User

def create_default_admin():
    """Create default admin user"""
    app = create_app('production')

    with app.app_context():
        try:
            # Check if admin already exists
            existing_admin = User.query.filter_by(is_admin=True).first()
            if existing_admin:
                print(f"Admin already exists: {existing_admin.username} ({existing_admin.email})")
                return

            # Create default admin
            admin = User(
                username='admin',
                email='admin@worker-management.com',
                is_admin=True
            )
            admin.set_password('admin123')

            db.session.add(admin)
            db.session.commit()

            print("✅ Default admin created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("Email: admin@worker-management.com")

        except Exception as e:
            print(f"❌ Error creating admin: {e}")
            db.session.rollback()

if __name__ == '__main__':
    create_default_admin()