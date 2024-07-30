from __future__ import annotations
from datetime import date
import numpy as np
from flask_login import UserMixin
from . import db

import numpy as np

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False) 
    password = db.Column(db.String(30), nullable = False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class LogedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))

 
class Land():
    first_point : list[float]
    second_point : list[float]
    third_point : list[float]
    fourth_point : list[float]

    def __init__(self, coords: list[list[float]]):
        self.first_point = coords[0]
        self.second_point = coords[1]
        self.third_point = coords[2]
        self.fourth_point = coords[3]
    
    def _sort_points(self) -> list[list[float]]:
        coordinates = [self.first_point, self.second_point, self.third_point, self.fourth_point]
        centroid = np.mean(coordinates, axis = 0)

        def angle_from_centroid(point):
            return np.arctan2(point[1] - centroid[1], point[0] - centroid[0])
        
        sorted_points = sorted(coordinates, key=angle_from_centroid)
        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = sorted_points
    
        return [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

    def get_area_surface(self) -> float:
        coordinates = self._sort_points()
        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = coordinates #nu stiu daca e legal ce am facut dar nu aveam alta idee pe moment
        #shoelace formula
        sum1 = x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1
        sum2 = y1 * x2 + y2 * x3 + y3 * x4 + y4 * x1
        return round((abs(sum1 - sum2) / 2), 2)
    
    def get_limits(self) -> list[float]:

        coords_as_np = np.array([self.first_point, 
                                 self.second_point,
                                 self.third_point,
                                 self.fourth_point])
        
        north = np.max(coords_as_np[:, 0])
        south = np.min(coords_as_np[:, 0])
        east = np.max(coords_as_np[:, 1])
        west = np.min(coords_as_np[:, 1])

        return [north, south, east, west]
    
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


   

