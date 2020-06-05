from app import db
from app import models


get_user = models.User.query.filter_by(username="test").first()

get_user.root_number="-1"
db.session.commit()