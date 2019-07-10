import random
from qsort import Qsort
from uuid import uuid4
import json


class Json:
    # TODO: add notSerializable validation

    @classmethod
    def encoder(cls, obj):
        if obj is None:
            return ''
        result = str()

        if isinstance(obj, dict):
            return cls._create_node(obj, '{', '}')
        elif isinstance(obj, tuple) or isinstance(obj, list):
            return cls._create_node(obj, '[', ']')
        elif isinstance(obj, str):
            result += '"{}"'.format(obj)
        else:
            result += '{}'.format(obj)

        return result

    @classmethod
    def decoder(cls, obj, result=None):
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
                    result[name] = cls.decoder(obj[name_to + 3:bracket_to + 1], list)
                    i = bracket_to
                i += 1
        elif isinstance(result, list):
            i = 0
            while i < len(obj):
                if obj[i] in '[{':
                    to = cls._find_closing_bracket(obj, i)
                    result.append(cls.decoder(obj[i:to + 1]))
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
            if string[i] == close_bracket:
                iter_bracket -= 1
            elif string[i] == open_bracket:
                iter_bracket += 1

            if iter_bracket == 0:
                return i

    @classmethod
    def _create_node(cls, obj, bracket, reverse_bracket):
        result = ''
        result += bracket
        if bracket == '{':
            for key, value in obj.items():
                result += cls.__string_check(key, value)
        elif bracket == '[':
            for value in obj:
                result += cls.__string_check(value)

        if len(result) > 1:
            return result[:-2] + reverse_bracket
        else:
            return result + reverse_bracket

    @classmethod
    def __string_check(cls, key, value=None):
        result = ''
        if isinstance(key, str):
            result += '"{}"'.format(key)
        else:
            result += '{}'.format(key)
        if value is not None:
            result += ': ' + Json.encoder(value)
        result += ', '
        return result


def main():
    #nums = [[i] for i in range(10)]
    #random.shuffle(nums)
    #print('Before: ' + str(nums))
    #print('After: ' + str(Qsort.sort(nums)))

    test_dict = {
        'list': [1, '2', "3", [4, 5, [[]]]],
        'tuple': (1, 2, [], 4),
        'dict': {
            'a': 'b',
            'c': 2
        },
        'empty_dict': {},
        3: 'name'
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
    encoded = json.dumps(test_list)
    decoded = json.loads(encoded)

    print('Standart dict to JSON: {}'.format(encoded))
    print('      My dict to json: {}\n'.format(Json.encoder(decoded)))
    print('Standart JSON to dict: {}'.format(decoded))
    print('      My JSON to dict: {}'.format(Json.decoder(encoded)))


if __name__ == "__main__":
    main()
