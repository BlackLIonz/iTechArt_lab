import random
from qsort import Qsort
from uuid import uuid4
import json


class JSONSerDes:
    # TODO: add notSerializable validation

    @classmethod
    def dumps(cls, obj, first=None):
        if obj is None:
            return ''
        elif first is None and not isinstance(obj, dict):
            raise TypeError
        result = str()
        if isinstance(obj, dict):
            return cls._create_node(obj, '{', '}')
        elif isinstance(obj, tuple) or isinstance(obj, list):
            return cls._create_node(obj, '[', ']')
        elif isinstance(obj, str):
            result += '"{}"'.format(obj)
        elif isinstance(obj, int):
            result += '{}'.format(obj)
        return result

    @classmethod
    def load(cls, obj, result=None):
        brackets = '[{"'
        if obj[0] in brackets:
            to = cls._find_closing_bracket(obj, 0)
            if obj[0] == '{':
                result = dict()
            elif obj[0] == '[':
                result = list()
            elif obj[0] == '"':
                result = str()
            obj = obj[1:to]
        elif obj[0].isdigit():
            result = int()
        if isinstance(result, dict):
            i = 0
            while i < len(obj):
                letter = obj[i]
                if obj[i] == '"':
                    name_to = cls._find_closing_bracket(obj, i)
                    name = obj[i + 1:name_to]
                    bracket_to = cls._find_closing_bracket(obj, name_to + 3)
                    result[name] = cls.load(obj[name_to + 3:bracket_to + 1])
                    i = bracket_to
                i += 1
        elif isinstance(result, list):
            i = 0
            while i < len(obj):
                if obj[i] in '[{':
                    to = cls._find_closing_bracket(obj, i)
                    result.append(cls.load(obj[i:to + 1]))
                    i = to
                elif obj[i].isdigit():
                    if i + 1 < len(obj):
                        if obj[i + 1] == '"':
                            result.append(obj[i])
                            i += 1
                            continue
                    result.append(int(obj[i]))
                i += 1
        elif isinstance(result, str):
            return obj
        elif isinstance(result, int):
            return int(obj)
        return result

    @classmethod
    def _find_closing_bracket(cls, string, start):
        open_bracket = string[start]

        if open_bracket == '{':
            close_bracket = '}'
        elif open_bracket == '[':
            close_bracket = ']'
        elif open_bracket == '"':
            close_bracket = '"'
        else:
            return start + 1
        iter_bracket = 1
        for i in range(start + 1, len(string)):
            if string[i] in close_bracket:
                iter_bracket -= 1
            elif string[i] in open_bracket:
                iter_bracket += 1

            if iter_bracket == 0:
                return i

    @classmethod
    def _create_node(cls, obj, bracket, reverse_bracket):
        result = ''
        result += bracket
        if bracket == '{':
            for key, value in obj.items():
                result += cls._string_check(key, value)
        elif bracket == '[':
            for value in obj:
                result += cls._string_check(value)

        if len(result) > 1:
            return result[:-2] + reverse_bracket
        else:
            return result + reverse_bracket

    @classmethod
    def _string_check(cls, key, value=None):
        result = ''
        if isinstance(key, str):
            result += '"{}"'.format(key)
        else:
            result += '{}'.format(key) if value is None else '"{}"'.format(key)
        if value is not None:
            result += ': {}'.format(JSONSerDes.dumps(value, 1))
        result += ', '
        return result


def main():

    test_dict = {
        'list': [1, '2', "3", [4, 5, [[]]]],
        'tuple': (1, 2, [], 4),
        'dict': {
            'a': 'b',
            'c': 2
        },
        'empty_dict': {},
        3: 'name',
        'num': 3
    }

    test_list = [1, 2, '4', [[[]]], {
        'list': [1, '2', "3", [4, 5, [[]]]],
        'tuple': (1, 2, [], 4),
        'dict': {
            'a': 'b',
            'c': 2
        },
        'empty_dict': {},
        3: 'name'
    }]
    encoded = json.dumps(test_dict)
    decoded = json.loads(encoded)

    my_encoded = JSONSerDes.dumps(test_dict)

    print('Standart dict to JSON: {}'.format(encoded))
    print('      My dict to json: {}\n'.format(my_encoded))
    print('Standart JSON to dict: {}'.format(decoded))
    print('      My JSON to dict: {}'.format(JSONSerDes.load(encoded)))


if __name__ == "__main__":
    main()
