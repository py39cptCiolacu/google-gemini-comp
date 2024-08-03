from __future__ import annotations
from datetime import date
from flask_login import UserMixin
from . import db

import numpy as np

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False) 
    password = db.Column(db.String(30), nullable = False)
    lands = db.relationship('Land', back_populates='owner')


class Land():
    # first_point : list[float]
    # second_point : list[float]
    # third_point : list[float]
    # fourth_point : list[float]

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', back_populates='lands')
    points = db.Column(db.JSON, nullable=False)

    def __init__(self, user_id, coords):
        self.user_id = user_id
        self.points = coords
    
    def _sort_points(self) -> list[list[float]]:
        coordinates = [self.first_point, self.second_point, self.third_point, self.fourth_point]
        centroid = np.mean(coordinates, axis = 0)

        def angle_from_centroid(point):
            return np.arctan2(point[1] - centroid[1], point[0] - centroid[0])
        
        sorted_points = sorted(coordinates, key=angle_from_centroid)
        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = sorted_points
    
        return [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

    def get_area_surface(self) -> float:
        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = self._sort_points() #nu stiu daca e legal ce am facut dar nu aveam alta idee pe moment
        #shoelace formula
        sum1 = x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1
        sum2 = y1 * x2 + y2 * x3 + y3 * x4 + y4 * x1
        return round((abs(sum1 - sum2) / 2), 2)

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



    

