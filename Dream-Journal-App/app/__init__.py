from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


# There are two kinds of "app" here, which is confusing.
# the package.
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# "from app" here refers to the whole package, as named by this file's
# parent directory. Putting our "import" statements down here is a
# workaround to avoid circular imports, because there are two things
# called "app". All of the other modules in our application must import
# the Flask app variable above. Putting imports at the bottom here
# allows all the modules to have their imports at the top. Yup, it's
# confusing.
from app import routes, models