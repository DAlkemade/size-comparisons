def parse_entry(line):
    return line.decode("utf-8").strip('\n')

def parse_yolo_file(fname):
    res = []
    with open(fname, 'rb') as input_file:
        for line in input_file:
            res.append(parse_entry(line))
    return res

def retrieve_names():
    return parse_yolo_file('data/9k.names')

def retrieve_labels():
    return parse_yolo_file('data/9k.labels')