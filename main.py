import argparse
import re
import itertools
import copy

ALLOWED_SYMBOLS = ['W', 'P', 'S', 'C']
WALL_SYMBOLS = ['/', '+', '|','-']


def read_file(path):
    map = []
    with open(path, "r") as file:
        for line in file:
            map.append(list(itertools.chain.from_iterable(line.replace(' ','_').rstrip())))
    return map


def find_room(map):
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == '_':
                return (x,y)
            else: 
                map[y][x] = 'X'
            

def print_map(map):
    for line in map:
        print(''.join(line))

def paint_room(coords, map):
    (start_x, start_y) = coords
    scan = True 
    symbol = True
    y = start_y
    x = start_x
    while scan:
        x = 0
        line = map[y]
        if y == start_y: line = line[start_x:]
        previous_symbol = ''
        while symbol:
            try: 
                symbol = line.pop(0)
            except IndexError:
                y += 1
                previous_symbol = ''
                break
            if symbol == 'X':
                pass
            elif symbol in WALL_SYMBOLS and previous_symbol not in WALL_SYMBOLS and previous_symbol != '':
                y += 1
                if DEBUG: 
                    print('prev: {}, curr: {}'.format(previous_symbol, symbol))
                    print('increasing y')
                previous_symbol = ''
                break
            elif symbol in WALL_SYMBOLS and previous_symbol in WALL_SYMBOLS:
                print (y, previous_symbol, symbol, line)
                return True
            else:
                if x > 1: map[y][x] = 'X'
                print_map(map)
            previous_symbol = symbol
            x += 1

def scan_room(coords, map):
    (start_x, start_y) = coords
    scan = True 
    symbol = True
    result = {}
    for symbol in ALLOWED_SYMBOLS:
        result.setdefault(symbol,0)
    y = start_y-1
    x = start_x
    while scan:
        x = 0
        y +=1
        line = copy.deepcopy(map[y])
        if y == start_y: 
            line = line[start_x:]
            x = start_x
        previous_symbol = ''
        while symbol:
            try: 
                symbol = line.pop(0)
            except IndexError:
                if x > 1: map[y][x-1] = 'X'
                if x > 0: map[y][x] = 'X'
                previous_symbol = ''
                break
            if symbol == 'X':
                pass
            elif symbol == '(':
                result['name'] = str(re.findall(r'\(.*?\)', symbol+''.join(line)))
                if DEBUG:
                    print('prev: {}, curr: {}, line: {}'.format(previous_symbol, symbol, ''.join(line)))
                    print('found room name {}'.format(result['name']))
                map[y][x:x+len(result['name'])-2] = ['X'] * (len(result['name'])-2)
            elif symbol in ALLOWED_SYMBOLS:
                result[symbol] += 1
            elif symbol in WALL_SYMBOLS and previous_symbol not in WALL_SYMBOLS and previous_symbol != '':
                if x > 1: map[y][x-1] = 'X'
                if x > 0: map[y][x] = 'X'
                if DEBUG: 
                    print('prev: {}, curr: {}'.format(previous_symbol, symbol))
                    print('increasing y')
                    print(''.join(line))
                previous_symbol = ''
                break
            elif symbol in WALL_SYMBOLS and previous_symbol in WALL_SYMBOLS:
                if x > 1: map[y][x-1] = 'X'
                
                return result
            if x > 1: map[y][x-1] = 'X'
            x+=1
            previous_symbol = symbol
    
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='furniture finder')
    parser.add_argument('-f', '--file', default=5, type=str, help='path to input file')
    parser.add_argument('-d', '--debug', action='store_true', help='Debugging mode')
    args = parser.parse_args()
    result = []
    DEBUG = args.debug
    map = read_file(args.file)
    result.append(scan_room(find_room(map),map))
    print_map(map)
    result.append(scan_room(find_room(map),map))
    print_map(map)
    print(find_room(map))
    # print(paint_room(find_room(map),map))