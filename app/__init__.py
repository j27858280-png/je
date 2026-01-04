from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Ensure database is in instance folder for persistence
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///:memory:'):
        print("⚠️  تحذير: تستخدم قاعدة بيانات في الذاكرة! البيانات ستُحذف عند إيقاف التطبيق.")
        print("   تأكد من تعيين FLASK_ENV=development أو إزالة DATABASE_URL من متغيرات البيئة.")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.instance_path}/worker_management.db'
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول أولاً'
    
    with app.app_context():
        try:
            # Import models
            from app.models import (User, Worker, WorkShift, ProductType, Production, 
                                    Sales, FuelLog, Medicine, Fertilizer, Consumption, Report,
                                    Attendance, Accounting, Role)
            
            # Create tables
            db.create_all()
            
            # Create default admin if none exists
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                # Ensure existing admin has proper permissions
                if not admin_user.is_admin:
                    admin_user.is_admin = True
                    db.session.commit()
                    print("Existing admin permissions fixed")
            else:
                # Create new default admin
                default_admin = User(
                    username='admin',
                    email='admin@worker-management.com',
                    is_admin=True
                )
                default_admin.set_password('admin123')
                db.session.add(default_admin)
                db.session.commit()
                print("Default admin created: username='admin', password='admin123'")
            
            # Register blueprints
            from app.routes import (main_bp, auth_bp, workers_bp, production_bp, 
                                    sales_bp, fuel_bp, medicines_bp, consumption_bp, 
                                    reports_bp, settings_bp, attendance_bp, accounting_bp, inject_now)
            
            app.register_blueprint(main_bp)
            app.register_blueprint(auth_bp)
            app.register_blueprint(workers_bp)
            app.register_blueprint(production_bp)
            app.register_blueprint(sales_bp)
            app.register_blueprint(fuel_bp)
            app.register_blueprint(medicines_bp)
            app.register_blueprint(consumption_bp)
            app.register_blueprint(reports_bp)
            app.register_blueprint(settings_bp)
            app.register_blueprint(attendance_bp)
            app.register_blueprint(accounting_bp)
            
            # Inject context
            app.context_processor(inject_now)
        except Exception as e:
            print(f"Error initializing app: {e}")
    
    return app
