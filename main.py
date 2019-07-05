from app import app
from app import db

from ads.blueprint import ads

import view

app.register_blueprint(ads, url_prefix="/board")

if __name__ == "__main__":
    app.run()
