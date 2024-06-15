from app import db, app, init
from app.view import *


if __name__ == '__main__':

    init(db)
    app.run(debug=True, host='0.0.0.0')
