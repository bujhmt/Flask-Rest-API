from sqlalchemy.orm.attributes import InstrumentedAttribute


def getModelEntityMappedKeys(item):
    mapped_values = {}
    for entity in item.__dict__.items():
        key = entity[0]
        value = entity[1]
        if key is not '_sa_instance_state':
            mapped_values[key] = value
    return mapped_values


def getModelKeys(instance):
    keys = []
    for entity in instance.__dict__.items():
        key = entity[0]
        key_type = entity[1]
        if type(key_type) is InstrumentedAttribute and key is not 'id' and not key[0].isupper():
            keys.append(key)
    return keys


def JSONEncoder(data: any):
    if isinstance(data, list):
        return [getModelEntityMappedKeys(item) for item in data]

    if isinstance(data, dict) or isinstance(data, object):
        return getModelEntityMappedKeys(data)
