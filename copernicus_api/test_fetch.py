from website.models import User, Land, db
from .fetch_request import get_cdsapi_infos

def test_fetch() -> None:

    test_user = User(
        username="test_username",
        email="email@test.com",
        password="parola_test"
    )

    db.session.add(test_user)
    db.session.commit()

    test_land = Land(
        name="test_land",
        user_id= test_user.id,
        x1 =12.928443545831145,
        y1 =  -85.69834828376771,
        x2 =12.928454002693616,
        y2 = -85.6976991891861,
        x3 =12.928020042532648,
        y3 = -85.69767773151398,
        x4 =12.928040956292639,
        y4 =  -85.69833219051363
    )

    db.session.add(test_land)
    db.session.commit()

    dict_infos = {"user" : test_user.id,
                        "land" : test_land.id ,
                        "parameters" : ['2m_temperature','2m_dewpoint_temperature'], 
                        "year": "2023", 
                        "month": ['01'],
                        "day" : ["01"],
                        "area" : ""
                        }
    
    get_cdsapi_infos(dict_infos)




