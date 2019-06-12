from app import app, db

db.init_app(app)

if __name__ == '__main__':
    # integrate SQLAlchemy to app
    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(port=5000, debug=True)
