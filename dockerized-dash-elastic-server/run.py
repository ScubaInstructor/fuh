from app import create_app, db
import logging
import sys

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from app.models import User
        db.create_all()  # Create database tables
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.DEBUG)

    app.run(debug=True, host="0.0.0.0") # TODO remove debug