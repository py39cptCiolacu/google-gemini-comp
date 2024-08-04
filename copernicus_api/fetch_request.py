import cdsapi
from website.models import User, Land
from nc_to_json import nc_to_json_convertor
from datetime import datetime

c = cdsapi.Client()

VALID_VARIABLES = [
            '2m_temperature',                    # Temperatura la 2 metri
            'total_precipitation',               # Precipitații totale
            'volumetric_soil_water_layer_1',     # Umiditatea solului (primul strat)
            'surface_solar_radiation_downwards', # Radiația solară la suprafață
            '2m_dewpoint_temperature',           # Umiditatea relativă
            '10m_u_component_of_wind',           # Viteza vântului (componenta u)
            '10m_v_component_of_wind',           # Viteza vântului (componenta v)
            'soil_temperature_level_1'           # Temperatura solului la nivelul 1
]

def check_fetch_infos(dict_infos: dict) -> dict | None:

    # dict_checked_infos = {"user" : "",
    #                     "land" : "",
    #                     "parameters" : [], 
    #                     "year": "2023", 
    #                     "month": ['01'],
    #                     "day" : ["01"],
    #                     "area" : ""
    #                     }
    
    must_have_keys = ["user", "land", "parameters", "year", "month", "day", "area"]
   
    for must_key in must_have_keys:
        if must_key not in dict_infos.keys():
            print(f"You are missing {must_key} for the dict")
            return None

    if dict_infos["user"] is None:
        print("User can not be NONE")
        return None

    if dict_infos["land"] is None:
        print("User can not be NONE")
        return None
    
    for var in dict_infos["parameters"]:
        print("Land can not None")
        if var not in VALID_VARIABLES:
            return None

    return dict_infos


def arrange_data(data_name: str) -> None:
    pass


def get_cdsapi_infos(dict_infos: dict) -> None:

    checked_infos = check_fetch_infos(dict_infos)

    if checked_infos is None:
        print("Something went wrong")
        return
    
    currrent_user = User.query.filter_by(id=dict_infos["user"]).first()
    current_land = Land.query.filter_by(id=dict_infos["land"]).first()
    now = datetime.now()
    file_name = currrent_user.usernamme + "_" + current_land.name + "_" + now.strftime("%Y_%m_%d_%H_%M_%S")

    c.retrieve(
        "reanalysis-era5-single-levels",  # Dataset-ul pe care vrei să-l accesezi
        {
            "product_type": 'reanalysis',
            "variable": checked_infos["parameters"],
            "year": checked_infos["year"],
            "month": checked_infos["month"],
            "day": checked_infos["day"],
            "time": ["00:00", "01:00", "02:00","03:00","04:00","05:00","06:00","07:00","08:00",
                     "09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00",
                     "18:00","19:00","20:00","21:00","22:00","23:00","24:00"],
            'area': checked_infos["day"],
            'format': 'netcdf'
        },
        f"{file_name}.nc")  # Numele fișierului în care vor fi salvate datele
    
    nc_to_json_convertor(file_name)
    # arrange_data(file_name)
    
    print("All good")


def test_fetch() -> None:
    pass
    

