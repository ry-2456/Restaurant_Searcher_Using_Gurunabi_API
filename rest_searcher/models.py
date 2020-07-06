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
    opening_hours = db.Column(db.Text)
    access = db.Column(db.String)
    holiday = db.Column(db.String)
    pr_long = db.Column(db.String)

    # parking_lots = db.Column(db.Integer)
    parking_lots = db.Column(db.String)

    budget = db.Column(db.String) # 平均予算
    party = db.Column(db.String) # ランチ平均予算
    lunch = db.Column(db.String) # 宴会・パーティ平均予算

    credit_card = db.Column(db.String)
    e_money = db.Column(db.String)
    
    coupon_pc_url = db.Column(db.String)
    coupon_mobile_url = db.Column(db.String)
    
    

    def __repr__(self):
        return "<Restaurant name={} img_url1={} img_url2={}".format(
            self.name, self.img_url1, self.img_url2)

db.create_all()

