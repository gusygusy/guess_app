import os

from flask import Flask

import secrets


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=secrets.token_bytes(32),
    #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)


from guess_app import Quiz
app.add_url_rule('/index', view_func=Quiz.as_view('index'))
return app

if __name__ == "__main__":
    app.run()
