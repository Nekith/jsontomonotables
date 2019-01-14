import sys
import json
from operator import itemgetter


def display_sep(output, columns):
    output.write('+')
    for c in columns:
        output.write('-')
        for i in range(0, c):
            output.write('-')
        output.write('-+')
    output.write('\n')


def display_legends(output, data):
    if 'legends' in data:
        for l in data['legends']:
            output.write(l + '\n')
        output.write('\n')


def order_data(data):
    if 'order' in data:
        column = data['order']['column'] if 'column' in data['order'] else 0
        reverse = data['order']['reverse'] if 'reverse' in data['order'] else False
        data['data'] = sorted(data['data'], key=itemgetter(column), reverse=reverse)
    return data


def jsontomonotables(filein, fileout):
    with open(filein, 'r') as data:
        data = json.load(data)
        data = order_data(data)
        with open(fileout, 'w') as output:
            display_legends(output, data)
            if 'data' in data:
                columns = []
                for i in range(0, len(data['data'][0])):
                    columns.append(0)
                for l in data['data']:
                    for i in range(0, len(l)):
                        if columns[i] < len(l[i]):
                            columns[i] = len(l[i])
                display_sep(output, columns)
                for l in data['data']:
                    output.write('|')
                    for c in range(0, len(l)):
                        output.write(' ')
                        output.write(l[c])
                        for i in range(0, columns[c] - len(l[c])):
                            output.write(' ')
                        output.write(' |')
                    output.write('\n')
                display_sep(output, columns)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: jsontomonotables.py [filein.json] [fileout.txt]')
    else:
        jsontomonotables(sys.argv[1], sys.argv[2])
