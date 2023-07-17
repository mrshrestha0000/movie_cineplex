# from fastapi import FastAPI
# from pydantic import BaseModel
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float

import datetime as _dt
import sqlalchemy as _sql 

import database as _database 



# Base = declarative_base()


class contact(_database.Base):
    __tablename__ = "contact"

    id= _sql.Column(_sql.Integer, primary_key=True, index=True)
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True, unique=True)
    phone_number = _sql.Column(_sql.String, index=True, unique=True)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

class theatre_info_model(_database.Base):
    __tablename__ = "theatre_info"

    # theatre_id = _sql.Column(_sql.Integer,primary_key=True, autoincrement=True)
    theatre_id = _sql.Column(_sql.Integer,primary_key=True)

    theatre_code = _sql.Column(_sql.String)
    theatre_name = _sql.Column(_sql.String) 
    location_id = _sql.Column(_sql.Integer)
    location_name = _sql.Column(_sql.String)
    address = _sql.Column(_sql.String)
    vat_number = _sql.Column(_sql.String)
    contact = _sql.Column(_sql.String)


# class theatre_auth_model(Base):
#     __tablename__ = "theatre_auth"

#     theatre_id : Column(Integer, ForeignKey('theatre_info.theatre_id'))
#     api_user : Column(String) 
#     api_password : Column(String) 
#     api_secret : Column(String) 
    
#     relation = relationship("theatre_info_model", backref="theatre_auth")


# class theatre_audi_model(Base):
#     __tbalename__ = "theatre_audi"

#     theatre_id : Column(Integer, ForeignKey('theatre_info.theatre_id'))
#     audi_id : Column(Integer, primary_key = True, autoincrement=True)
#     audi_name : Column(String)
#     audi_total_seat : Column(Integer)
#     row : Column(Integer)
#     column : Column(Integer)

#     relation = relationship("theatre_info_model", backref="theatre_audi")


# class movie_model(Base):
#     __tablename__ = "movie"

#     theatre_id : Column(Integer, ForeignKey('theatre_info.theatre_id'))

#     movie_id : Column(Integer, primary_key=True)
#     movie_name : Column(String)
#     movie_type : Column(String)
#     duration : Column(int) # in min
#     image : Column(String) # Path to image file

#     relation = relationship("theatre_info_model", backref="movie")


# class show_model(Base):
#     __tablename__ = "show"

#     movie_id : Column(Integer, ForeignKey('movie.movie_id'))
#     audi_id : Column(Integer, ForeignKey('theatre_audi.audi_id'))

#     show_id : Column(Integer, primary_key = True, autoincrement = True) 
#     startTime : Column(DateTime)
#     show_status : Column(String)
#     ticket_price : Column(float)

#     movie = relationship("theatre_info_model", backref="show") 
#     theatre_audi = relationship("theatre_audi_model", backref="show")


# class seat_detail_model(Base):
#     __tablename__ = "seat_detail"

#     seat_id : Column(Integer)
#     audi_id :  Column(Integer, ForeignKey('theatre_audi.audi_id')) 
#     show_id : Column(Integer, ForeignKey('show.show_id'))
#     row : Column(Integer)
#     colon : Column(Integer)
#     is_active : Column(bool)
#     ticket_type : Column(Integer)   # 1 - platinium , 2 - gold 
#     price : Column (Float)

#     audi = relationship("theatre_audi_model", backref="seat_detail")
#     show_id = relationship("show_model", backref="seat_detail")

    
# class seat_hold_model(Base):
#     __tablename__ = "seat_hold"

#     seat_hold_id : Column(Integer, primary_key = True, autoincrement=True)
    
#     seat_id : Column(Integer, ForeignKey('seat_detail.seat_id'))
#     audi_id :  Column(Integer, ForeignKey('theatre_audi.audi_id')) 
#     show_id : Column(Integer, ForeignKey('show.show_id'))
#     exiary_time : Column(DateTime)

#     transaction_id : Column(Integer)

#     seat_id = relationship("seat_detail_model", backref='seat_hold')
#     audi_id = relationship("theatre_audi_model", backref="seat_hold")
#     show_id = relationship("show_model", backref="seat_hold")


# class purchase_ticket_model(Base):
#     __tablename__ = "purchase_ticket"

#     ticket_id : Column(Integer, primary_key = True, autoincrement = True)
#     amount : Column(float)
#     transaction_id : Column(Integer)

#     seat_id : Column(Integer, ForeignKey('seat_detail.seat_id'))
#     audi_id :  Column(Integer, ForeignKey('theatre_audi.audi_id')) 
#     show_id : Column(Integer, ForeignKey('show.show_id'))

#     seat_id = relationship("seat_detail_model", backref='purchase_ticket')
#     audi_id = relationship("theatre_audi_model", backref="purchase_ticket")
#     show_id = relationship("show_model", backref="purchase_ticket")


        


# # ticket_generate 
# #     ticket_generate_id 
# #     show_name
# #     time
# #     audi
# #     seat_no
# #     price
# #     ticket_code - unique - bar code / qr code 


# # transaction_detail
# #     txn_id
# #     purchase_id
# #     ticket_number