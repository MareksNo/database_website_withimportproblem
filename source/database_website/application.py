import flask

from flask_migrate import Migrate

from database_website.extensions.database import db
from database_website.properties import navigation_bar


class Application(flask.Flask):
    def create_migrations(self):
        migrate = Migrate(self, db)

    def load_configuration(self):
        self.config.from_pyfile('configuration.py')

    def configure_database(self):
        from database_website.extensions.database import db

        db.init_app(app=self)

    def configure_login_manager(self):
        from database_website.extensions.auth import login_manager

        login_manager.init_app(app=self)

    def register_applications(self):
        from database_website.applications.core.urls import blueprint as core_blueprint
        from database_website.applications.users.urls import blueprint as users_blueprint
        from database_website.applications.products.urls import blueprint as products_blueprint
        from database_website.commands import blueprint as commands_blueprint
        from database_website.properties import blueprint as properties_blueprint
        from database_website.applications.errors.errors import blueprint as errors_blueprint

        self.register_blueprint(blueprint=users_blueprint)
        self.register_blueprint(blueprint=products_blueprint)
        self.register_blueprint(blueprint=core_blueprint)
        self.register_blueprint(blueprint=commands_blueprint)
        self.register_blueprint(blueprint=properties_blueprint)
        self.register_blueprint(blueprint=errors_blueprint)

    @classmethod
    def create(cls):
        instance = Application(__name__)

        instance.load_configuration()
        instance.configure_database()
        instance.configure_login_manager()
        instance.register_applications()
        instance.create_migrations()

        return instance


application = Application.create()


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def sitemap():
    links = []
    for rule in application.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = flask.url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return links


@application.context_processor
def inject_endpoints():
    return dict(endpoints=sitemap())


application.run()


'''
To do:

Somehow split context_processor, sitemap and cli commands in seperate Files.
Get requirements of a request // Possible solution 
https://stackoverflow.com/questions/5489649/check-if-a-function-has-a-decorator - Still doesn't solve a different issue
Blueprints could be a possible solution
Fixed.

Add a random object using a decimal value, if error - SQLAlchemy doesnt allow decimal in integer fields,
else, forms does something wierd.
 
Lines  50-70, do not seem to be used. 

Figure out/research, how the server_default gets defined and used.
 
So many things to do. Get to work me lol.
'''
