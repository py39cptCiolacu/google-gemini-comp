import cdsapi
from website.models import User, Land

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

    dict_checked_infos = {"user" : "",
                        "land" : "",
                        "parameters" : [], 
                        "year": "2023", 
                        "month": ['01'],
                        "day" : ["01"],
                        "area" : ""
                        }
    
    if dict_infos["user"] is None:
        return None

    if dict_infos["land"] is None:
        return None
    
    for var in dict_infos["parameters"]:
        if var not in VALID_VARIABLES:
            return None

    return dict_checked_infos


def get_cdsapi_infos() -> None:

    checked_infos = check_fetch_infos()

    if checked_infos is None:
        print("Something went wrong")
        return
 
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
        "download.nc")  # Numele fișierului în care vor fi salvate datele

    print("All good")
