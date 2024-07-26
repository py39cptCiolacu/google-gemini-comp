from __future__ import annotations
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from . import db

import numpy as np

# Admin si User cred ca pot fi acealsi clasa si sa folosim inheritance sau composition
# deocamdata sunt separate pt security
# mai trebuie oricum sa faca inheritence de la ceva din sqlalchemy ca sa le putem folosi la login

#class Admin(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(30), nullable = False)
#    email = db.Column(db.String(50), unique = True, nullable = False) 
#    dummy_passord = db.Column(db.String(30), nullable = False)
#    _password = db.Column("password", nullable = False)
#
#    @property
#    def password(self) -> str:
#        return self._password
#
#    @password.setter
#    def password(self, plaitext_password: str) -> None:
#        self._password = generate_password_hash(plaitext_password)
#
#    def check_password(self, plaintext_password: str) -> bool:
#        return check_password_hash(self._password, plaintext_password)



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), nullable = False)
#     email = db.Column(db.String(50), unique = True, nullable = False) 
#     dummy_passord = db.Column(db.String(30), nullable = False)
#     _password = db.Column("password", nullable = False)

#     @property
#     def password(self) -> str:
#         return self._password

#     @password.setter
#     def password(self, plaitext_password: str) -> None:
#         self._password = generate_password_hash(plaitext_password)

#     def check_password(self, plaintext_password: str) -> bool:
#         return check_password_hash(self._password, plaintext_password)


class Land():
    first_point : str # cred ca nu le vom stoca ca str
    second_point : str
    third_point : str
    fourth_point : str

    def get_point_array(self) -> list:
        x1, y1 = map(float, self.first_point.split(", "))
        x2, y2 = map(float, self.second_point.split(", "))
        x3, y3 = map(float, self.third_point.split(", "))
        x4, y4 = map(float, self.fourth_point.split(", "))

        coordinates = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        return coordinates

    def get_area_surface(self) -> int:
        coordinates = self.get_point_array()
        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = coordinates #nu stiu daca e legal ce am facut dar nu aveam alta idee pe moment
        #shoelace formula
        sum1 = x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1
        sum2 = y1 * x2 + y2 * x3 + y3 * x4 + y4 * x1
        return (abs(sum1 - sum2) / 2)

    #info: un json cu 2-3 chestii random


class Result():
    input : str   #poate va fi un JSON
    result : str 
    statisfaction_level: int
    generated_date: date

    def _clear_result(self) -> None:
        # __del__ cred ca trebuie apelat
        pass

    def __del__(self) -> None:
        pass



    

