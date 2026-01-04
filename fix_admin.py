#!/usr/bin/env python3
"""
Fix admin permissions immediately
إصلاح صلاحيات الإدمن فوراً
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User

def fix_admin_permissions():
    """Fix admin permissions immediately"""
    app = create_app('production')

    with app.app_context():
        print("🔧 إصلاح صلاحيات الإدمن...")

        # Find admin user
        admin_user = User.query.filter_by(username='admin').first()

        if admin_user:
            if not admin_user.is_admin:
                admin_user.is_admin = True
                db.session.commit()
                print("✅ تم إصلاح صلاحيات الإدمن!")
            else:
                print("✅ الإدمن لديه الصلاحيات المطلوبة")
        else:
            print("❌ لم يتم العثور على مستخدم 'admin'")

        # Show current status
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print(f"👤 المستخدم: {admin_user.username}")
            print(f"🔐 إدمن: {'نعم' if admin_user.is_admin else 'لا'}")
            print(f"✏️  صلاحية التعديل: {'نعم' if admin_user.has_permission('edit_workers') else 'لا'}")

if __name__ == '__main__':
    fix_admin_permissions()