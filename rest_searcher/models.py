from rest_searcher import db

class Restaurant(db.Model):

    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    img_url1 = db.Column(db.String)
    img_url2 = db.Column(db.String)
    address = db.Column(db.String)
    tel = db.Column(db.String)
    # opening_hours = db.Column(String)
    budget = db.Column(db.Integer) # 平均予算
    opening_hours = db.Column(db.Text)

    def __repr__(self):
        return "<Restaurant name={} img_url1={} img_url2={}".format(
            self.name, self.img_url1, self.img_url2)

db.create_all()

