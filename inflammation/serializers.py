# file: inflammation/serializers.py

import json
import inflammation.models as models
from abc import ABC
import csv

class Serializer(ABC):
    @classmethod
    def serialize(cls, instances):
        raise NotImplementedError

    @classmethod
    def save(cls, instances, path):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data):
        raise NotImplementedError

    @classmethod
    def load(cls, path):
        raise NotImplementedError

class PatientSerializer(Serializer):
    model = models.Patient

    @classmethod
    def serialize(cls, instances):
        return [{
            'name': instance.name,
            'observations': ObservationSerializer.serialize(instance.observations),
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        instances = []

        for item in data:
            item['observations'] = ObservationSerializer.deserialize(item.pop('observations'))
            instances.append(cls.model(**item))

        return instances



class PatientJSONSerializer(PatientSerializer):
    @classmethod
    def save(cls, instances, path):
        with open(path, 'w') as jsonfile:
            json.dump(cls.serialize(instances), jsonfile)

    @classmethod
    def load(cls, path):
        with open(path) as jsonfile:
            data = json.load(jsonfile)

        return cls.deserialize(data)

    @classmethod 
    def display(cls,path):
        with open(path) as jsonfile:
            data = json.load(jsonfile)

        for i in data:
            print(i)
            print('new ')

class PatientCSVSerializer(PatientSerializer):
    @classmethod
    def save(cls, instances, path):
        with open(path,'w', newline='') as csvfile:

            for i in cls.serialize(instances):
                # foreach patient
                csvfile.write("%s,%s,%s"%('name',i['name'],'observations'))
                
                for j in i['observations']:
                    # for each observation
                    csvfile.write(",%s,%s,%s,%s"%('day',j['day'],'value',j['value']))
                csvfile.write("\n")
                

    @classmethod 
    def load(cls,path):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                data.append({'date': row['date'], 'value': row['value']})


class ObservationSerializer(Serializer):
    model = models.Observation

    @classmethod
    def serialize(cls, instances):
        return [{
            'day': instance.day,
            'value': instance.value,
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        return [cls.model(**d) for d in data]

