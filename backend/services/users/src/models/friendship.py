from app import db, ma


class Friendship(db.Model):
    __tablename__ = "friendships"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", foreign_keys=[user_id])
    friend = db.relationship("User", foreign_keys=[friend_id])

    # add constraint to prevent duplicate friendships
    __table_args__ = (
        db.UniqueConstraint("user_id", "friend_id", name="unique_friendship"),
    )


class FriendshipSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Friendship
        load_instance = True
        sqla_session = db.session
        include_fk = True



friendship_schema = FriendshipSchema()
friendships_schema = FriendshipSchema(many=True)
