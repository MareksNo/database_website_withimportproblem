from database_website.extensions.database import db


class Product(db.Model):
    id_product = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    seller_username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    description = db.Column(db.Text, nullable=True, default='No Info')

    def __repr__(self):
        return f"Product('{self.product_name}', '{self.price}')"

    __table_args__ = {'extend_existing': True}

    @classmethod
    def add_product(cls, product_name, price, seller_username, description):

        instance = cls(
            product_name=product_name,
            price=price,
            seller_username=seller_username,
            description=description,
        )

        db.session.add(instance)
        db.session.commit()

    def delete_product(self):

        db.session.delete(self)
        db.session.commit()
