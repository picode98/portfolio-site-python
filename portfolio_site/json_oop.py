import datetime
from typing import Dict, get_args, get_origin, Iterable, List


class JSONDeserializable:
    def __init__(self, **members):
        self.__dict__.update(members)

    @classmethod
    def from_json_dict(cls, json_dict: Dict, **context_members):
        class_keys = cls.__annotations__

        matching_keys = set(class_keys.keys()).intersection(json_dict.keys())
        result_kwargs = {}

        for key in matching_keys:
            this_class = get_origin(class_keys[key])
            if this_class is None:
                this_class = class_keys[key]

            if issubclass(this_class, JSONDeserializable):
                result_kwargs[key] = this_class.from_json_dict(json_dict[key], **context_members)
            elif issubclass(this_class, datetime.date):
                result_kwargs[key] = datetime.datetime.strptime(json_dict[key], getattr(cls, key + '_format')).date()
            elif issubclass(this_class, datetime.datetime):
                result_kwargs[key] = datetime.datetime.strptime(json_dict[key], getattr(cls, key + '_format'))
            elif issubclass(this_class, Iterable) and isinstance(json_dict[key], List)\
                    and len(get_args(class_keys[key])) == 1 and issubclass(get_args(class_keys[key])[0], JSONDeserializable):
                result_kwargs[key] = this_class(get_args(class_keys[key])[0].from_json_dict(item, **context_members) for item in json_dict[key])
            else:
                result_kwargs[key] = this_class(json_dict[key])

        result_kwargs.update(context_members)
        return cls(**result_kwargs)
