import sqlalchemy as sqlalchemy
import database as _database
from sqlalchemy.orm import relationship, Mapped


class theatre_info_model(_database.Base):
    __tablename__ = "theatre_info"

    theatre_id: Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )

    theatre_code = sqlalchemy.Column(sqlalchemy.String)
    theatre_name = sqlalchemy.Column(sqlalchemy.String)
    location_id = sqlalchemy.Column(sqlalchemy.Integer)
    location_name = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    vat_number = sqlalchemy.Column(sqlalchemy.String)
    contact = sqlalchemy.Column(sqlalchemy.String)


class theatre_auth_model(_database.Base):
    __tablename__ = "theatre_auth"

    theatre_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("theatre_info.theatre_id"),
        primary_key=True,
    )
    api_username = sqlalchemy.Column(sqlalchemy.String)
    api_password = sqlalchemy.Column(sqlalchemy.String)
    api_secret = sqlalchemy.Column(sqlalchemy.String)

    relation: Mapped["theatre_info_model"] = relationship(
        "theatre_info_model", backref="theatre_auth"
    )


class theatre_audi_model(_database.Base):
    __tablename__ = "theatre_audi"

    theatre_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("theatre_info.theatre_id")
    )
    audi_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    audi_name = sqlalchemy.Column(sqlalchemy.String)
    audi_total_seat = sqlalchemy.Column(sqlalchemy.Integer)
    row = sqlalchemy.Column(sqlalchemy.Integer)
    column = sqlalchemy.Column(sqlalchemy.Integer)
    audi_seat_type = sqlalchemy.Column(sqlalchemy.String)

    relation: Mapped["theatre_info_model"] = relationship(
        "theatre_info_model", backref="theatre_audi"
    )


class seat_detail_model(_database.Base):
    __tablename__ = "seat_detail"

    seat_name = sqlalchemy.Column(sqlalchemy.String, primary_key=True, unique=True)
    theatre_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("theatre_info.theatre_id")
    )
    seat_id = sqlalchemy.Column(sqlalchemy.String)
    audi_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("theatre_audi.audi_id")
    )
    row = sqlalchemy.Column(sqlalchemy.Integer)
    column = sqlalchemy.Column(sqlalchemy.Integer)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean)
    seat_type = sqlalchemy.Column(sqlalchemy.String)
    total_seat = sqlalchemy.Column(sqlalchemy.Integer)
    seat_status = sqlalchemy.Column(sqlalchemy.Integer)

    relation: Mapped["theatre_info_model"] = relationship(
        "theatre_info_model", backref="seat_detail"
    )
    relation: Mapped["theatre_audi_model"] = relationship(
        "theatre_audi_model", backref="seat_detail"
    )


class movie_model(_database.Base):
    __tablename__ = "movie"

    theatre_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("theatre_info.theatre_id")
    )
    movie_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    movie_name = sqlalchemy.Column(sqlalchemy.String)
    movie_type = sqlalchemy.Column(sqlalchemy.String)
    duration = sqlalchemy.Column(sqlalchemy.Integer)
    image = sqlalchemy.Column(sqlalchemy.String)

    relation: Mapped["theatre_info_model"] = relationship(
        "theatre_info_model", backref="movie"
    )


class show_model(_database.Base):
    __tablename__ = "show"

    theatre_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("theatre_info.theatre_id")
    )
    movie_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("movie.movie_id")
    )
    audi_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("theatre_audi.audi_id")
    )
    show_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    startTime = sqlalchemy.Column(sqlalchemy.DateTime)
    show_status = sqlalchemy.Column(sqlalchemy.String)
    ticket_price = sqlalchemy.Column(sqlalchemy.Float)

    relation: Mapped["theatre_info_model"] = relationship(
        "theatre_info_model", backref="show"
    )
    relation: Mapped["theatre_audi_model"] = relationship(
        "theatre_audi_model", backref="show"
    )


# class seat_hold_model(_database.Base):
#     __tablename__ = "seat_hold"

#     seat_hold_id = sqlalchemy.Column(
#         sqlalchemy.Integer, primary_key=True, autoincrement=True
#     )
#     seat_name = sqlalchemy.Column(
#         sqlalchemy.String, sqlalchemy.ForeignKey("seat_detail.seat_name")
#     )
#     show_id = sqlalchemy.Column(sqlalchemy.Integer)
#     exipry_time = sqlalchemy.Column(sqlalchemy.DateTime)
#     transaction_id = sqlalchemy.Column(sqlalchemy.String)
#     api_username = sqlalchemy.Column(sqlalchemy.String)

#     relation: Mapped["seat_detail_model"] = relationship(
#         "seat_detail_model", backref="seat_hold"
#     )


class purchase_ticket_model(_database.Base):
    __tablename__ = "purchase_ticket"

    ticket_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    amount = sqlalchemy.Column(sqlalchemy.Float)
    transaction_id = sqlalchemy.Column(sqlalchemy.Integer)
    seat_name = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("seat_detail.seat_name")
    )
    audi_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("theatre_audi.audi_id")
    )
    show_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("show.show_id")
    )
    api_username = sqlalchemy.Column(sqlalchemy.String)

    relation: Mapped["seat_detail_model"] = relationship(
        "seat_detail_model", backref="purchase_ticket"
    )
