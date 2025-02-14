from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from app.models import User
        db.create_all()  # Create database tables

    app.run(debug=True, host="0.0.0.0") # TODO remove debug