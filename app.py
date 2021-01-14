from flask import Flask
from config import Config
from database.db import session, recreate_database
from routes.api.user import users

app = Flask(__name__)
app.register_blueprint(users)

@app.route('/')
def hello_world():
    return '''<h1>'Hello World!'</h1>'''


@app.route('/recreate', methods=['POST'])
def recreate(exception=None):
    if exception: print('Recreate Error! ', exception)
    recreate_database()
    return 'Recreated!', 201



@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception: print(exception)
    session.close()


if __name__ == '__main__':
    app.run(host=Config.app_host, port=Config.app_port)
