from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.analyze import retrieve_synset

inputparser = InputsParser()
yolo_synset_ids = inputparser.retrieve_labels()
yolo_synset_names = [retrieve_synset(label)._name for label in yolo_synset_ids]


vg_synset_dict = inputparser.parse_json('visual_genome_object_synsets.json')
vg_synset_ids = list(vg_synset_dict.values())


def intersection(list1: list, list2: list):
    return list(set(list1) & set(list2))


overlap = intersection(vg_synset_ids, yolo_synset_names)
print(f'Yolo size: {len(yolo_synset_names)}')
print(f'VG size: {len(vg_synset_ids)}')
print(f'Intersection size: {len(overlap)}')