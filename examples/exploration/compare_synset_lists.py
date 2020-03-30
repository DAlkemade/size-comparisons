from size_comparisons.exploration.compare_synset_lists import intersection, SynsetsExploration
from size_comparisons.parse_objects import InputsParser
import pprint

pp = pprint.PrettyPrinter()

exploration = SynsetsExploration(InputsParser())
exploration.retrieve_reformat_lists()

intersection_yolo_imagenet = intersection(exploration.yolo_synset_names, exploration.imagenet_synset_names)

print(f'Intersection imagenet and yolo: {len(intersection_yolo_imagenet)}')


vg_synset_ids = exploration.vg_synset()

intersection_yolo_vg = intersection(vg_synset_ids, exploration.yolo_synset_names)

print(f'Yolo size: {len(exploration.yolo_synset_names)}')
print(f'VG size: {len(vg_synset_ids)}')
print(f'Intersection size: {len(intersection_yolo_vg)}')

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




