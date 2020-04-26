from size_comparisons.exploration.compare_synset_lists import intersection, SynsetsExploration
from size_comparisons.parse_objects import InputsParser
import pprint
import pandas as pd

pp = pprint.PrettyPrinter()

exploration = SynsetsExploration(InputsParser())
exploration.retrieve_reformat_lists()

intersection_yolo_imagenet = intersection(exploration.yolo_synset_names, exploration.imagenet_synset_names)

print(f'Intersection imagenet and yolo: {len(intersection_yolo_imagenet)}')


vg_synset_ids = exploration.vg_synset()

intersection_yolo_vg = intersection(vg_synset_ids, exploration.yolo_synset_names)
pp.pprint(intersection_yolo_vg)
with open('VG_YOLO_intersection.txt', 'w') as f:
    for item in intersection_yolo_vg:
        f.write("%s\n" % item.split('.')[0].replace('_', " "))

print(f'Yolo size: {len(exploration.yolo_synset_names)}')
print(f'VG size: {len(vg_synset_ids)}')

three_way_intersection = intersection(vg_synset_ids, intersection_yolo_imagenet)
print(f'3-way intersection size: {len(three_way_intersection)}')
# pp.pprint(three_way_intersection)

blcs = exploration.blcs()

# pp.pprint(blcs)
print(f'Number of blcs: {len(blcs)}')
three_way_intersection_blc = intersection(three_way_intersection, blcs)
print(f'Intersection BLC and 3-way intersection: {len(three_way_intersection_blc)}')
# pp.pprint(three_way_intersection_blc)

yolo_blc_intersection = intersection(exploration.yolo_synset_names, blcs)
print(f'Intersection BLC and yolo: {len(yolo_blc_intersection)}')
# pp.pprint(yolo_blc_intersection)

vg_blc_intersection = intersection(exploration.vg_synset_names, blcs)
print(f'Intersection BLC and vg: {len(vg_blc_intersection)}')
# pp.pprint(vg_blc_intersection)




