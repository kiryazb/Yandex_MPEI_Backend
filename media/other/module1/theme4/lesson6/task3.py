mobile_devices = {
    'cucuPhone': 2010,
    'cucuBlet': 2013,
    'cucuClock': 2015,
    'cucuEar': 2018,
    'cuCube': 2015,
}

home_devices = {
    'cucuLot': 2011,
    'cucuBlock': 2010,
    'cucuWall': 2010,
    'cucuMonitor': 2020,
    'cucuLamp': 2015,
    'cucuTable': 2016,
    'cucuTV': 2017,
}

not_supported_devices = {'cucuBlock', 'cucuBlet', 'cucuWall'}

result_catalog = {}



# Допишите функцию выборки поддерживаемого девайса из словаря
def get_supported_catalog(dict_devices, device):
    supported_catalog = {}
    if device in dict_devices:
        supported_catalog[device] = dict_devices[device]
    return supported_catalog


all_devices = set(mobile_devices.keys()) | set(home_devices.keys())
supported_devices = {device for device in all_devices if device not in not_supported_devices}

print(all_devices)

for device in supported_devices:
    supported_mob_dev = get_supported_catalog(mobile_devices, device)
    # Добавьте значение в словарь result_catalog
    result_catalog.update(supported_mob_dev)
    supported_home_dev = get_supported_catalog(home_devices, device)
    # Добавьте значение в словарь result_catalog
    result_catalog.update(supported_home_dev)


print('Каталог поддерживаемых девайсов: ')
print(result_catalog)
