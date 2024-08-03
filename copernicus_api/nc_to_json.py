import xarray as xr
import json

# Deschide fișierul NetCDF
ds = xr.open_dataset('download.nc')

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
with open('output_file.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print("Conversia a fost realizată cu succes!")
