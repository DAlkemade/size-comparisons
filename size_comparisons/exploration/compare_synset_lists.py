import re

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.analyze import retrieve_synset


def intersection(list1: list, list2: list):
    return list(set(list1) & set(list2))


class SynsetsExploration:
    def __init__(self, inputparser: InputsParser):
        self._inputparser = inputparser
        self.yolo_synset_names = None
        self.blc_synset_names = None
        self.vg_synset_names = None
        self.imagenet_synset_names = None

    def retrieve_reformat_lists(self):
        yolo_synset_ids = self.yolo_synset_ids()
        imagenet_detection_synset_ids = self.imagenet_detection()

        self.yolo_synset_names = [retrieve_synset(label)._name for label in yolo_synset_ids]
        self.imagenet_synset_names = [retrieve_synset(label)._name for label in imagenet_detection_synset_ids]
        self.blc_synset_names = self.blcs()
        self.vg_synset_names = self.vg_synset()

    def imagenet_detection(self):
        with open(self._inputparser.data_dir / 'imagenet.bbox.obtain_synset_wordlist',
                  'rb') as f:  # around 3000 classes. is what R-FCN-3000 uses
            imagenet_detection_synsets = []
            for line in f:
                line = str(line)
                match = re.search(r'wnid=(.*)"', line)
                id = match.group(1)
                imagenet_detection_synsets.append(id)

        return imagenet_detection_synsets

    def yolo_synset_ids(self):
        return self._inputparser.retrieve_labels()

    def vg_synset(self):
        vg_synset_dict = self._inputparser.parse_json('visual_genome_object_synsets.json')
        return list(vg_synset_dict.values())

    def blcs(self):
        with open(self._inputparser.data_dir / 'predicted_basic_level_categories_synsets.txt', 'rb') as f:
            blcs = []
            for line in f:
                line = str(line)
                match = re.search(r"b.(.*[0-9]+)", line)
                id = match.group(1)
                blcs.append(id)
        return blcs
