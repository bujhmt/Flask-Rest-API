def getModelEntityMappedKeys(item):
    mapped_values = {}
    for entity in item.__dict__.items():
        key = entity[0]
        value = entity[1]
        if key is not '_sa_instance_state':
            mapped_values[key] = value
    return mapped_values


def JSONEncoder(data: any):
    if isinstance(data, list):
        return [getModelEntityMappedKeys(item) for item in data]

    if isinstance(data, dict) or isinstance(data, object):
        return getModelEntityMappedKeys(data)
