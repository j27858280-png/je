import os
import click
from app import create_app, db
from app.models import User

app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

@app.cli.command()
@click.option('--username', prompt='Enter admin username', help='Admin username')
@click.option('--email', prompt='Enter admin email', help='Admin email')
@click.option('--password', prompt='Enter admin password', hide_input=True, confirmation_prompt=True, help='Admin password')
def create_admin(username, email, password):
    """Create an admin user."""
    if User.query.filter_by(username=username).first():
        print('Admin user already exists!')
        return
    
    admin = User(username=username, email=email, is_admin=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    
    print(f'Admin user {username} created successfully!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
