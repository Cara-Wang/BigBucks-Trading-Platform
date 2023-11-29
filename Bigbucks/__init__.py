import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "bigbucks.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from BigBucks import db
    db.init_app(app)

    # Use blueprint to seperate functions
    from BigBucks import auth, member, administrator
    app.register_blueprint(auth.bp) #auth is the login/register part
    app.register_blueprint(member.bp) #Now member just provides a blank index page
    app.register_blueprint(administrator.bp)

    app.add_url_rule("/", endpoint="index")



    from . import db
    db.init_app(app)
    
    return app
