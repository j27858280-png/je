#!/usr/bin/env python3
"""
Check and fix admin permissions
فحص وإصلاح صلاحيات الإدمن
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User

def check_admin_permissions():
    """Check and fix admin permissions"""
    app = create_app('production')

    with app.app_context():
        print("=" * 60)
        print("🔍 فحص صلاحيات الإدمن")
        print("=" * 60)

        # Get all users
        users = User.query.all()

        if not users:
            print("❌ لا يوجد أي مستخدمين في النظام!")
            return

        print(f"📊 عدد المستخدمين: {len(users)}")
        print()

        for user in users:
            print(f"👤 المستخدم: {user.username}")
            print(f"📧 البريد: {user.email}")
            print(f"🔐 إدمن: {'نعم' if user.is_admin else 'لا'}")
            print(f"✅ نشط: {'نعم' if user.is_active else 'لا'}")

            # Check permissions
            has_edit_workers = user.has_permission('edit_workers')
            has_add_workers = user.has_permission('add_workers')
            print(f"✏️  صلاحية التعديل: {'نعم' if has_edit_workers else 'لا'}")
            print(f"➕ صلاحية الإضافة: {'نعم' if has_add_workers else 'لا'}")

            # Fix if needed
            if not user.is_admin and user.username == 'admin':
                print("🔧 إصلاح: جعل المستخدم إدمن...")
                user.is_admin = True
                db.session.commit()
                print("✅ تم إصلاح الصلاحيات!")

            print("-" * 40)

        print("\n" + "=" * 60)
        print("✅ انتهى الفحص")
        print("=" * 60)

if __name__ == '__main__':
    check_admin_permissions()