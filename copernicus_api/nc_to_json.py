import xarray as xr
import json
import os


def nc_to_json_convertor(nc_file_name: str) -> None:

    # Deschide fișierul NetCDF
    ds = xr.open_dataset(nc_file_name)

    # Crearea unui dicționar pentru a stoca datele
    data_dict = {}

    # Iterarea prin toate variabilele din dataset și adăugarea lor în dicționar
    for var_name in ds.variables:
        data_dict[var_name] = ds[var_name].values.tolist()

    # Adăugarea atributelor datasetului (metadate)
    data_dict['attributes'] = {attr: ds.attrs[attr] for attr in ds.attrs}

    for key in data_dict.keys():
        print(key)

    # Scrierea datelor în format JSON
    with open(f'{nc_file_name}.json', 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)


    os.remove(f"{nc_file_name}.nc")

    print("Conversia a fost realizată cu succes!")
