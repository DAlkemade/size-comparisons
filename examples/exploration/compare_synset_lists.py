from size_comparisons.exploration.compare_synset_lists import intersection, SynsetsExploration
from size_comparisons.parse_objects import InputsParser

import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os

set_up_root_logger(f'COMPARE_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)

def main():
    exploration = SynsetsExploration(InputsParser())
    exploration.retrieve_reformat_lists()

    intersection_yolo_imagenet = intersection(exploration.yolo_synset_names, exploration.imagenet_synset_names)

    logger.info(f'Intersection imagenet and yolo: {len(intersection_yolo_imagenet)}')


    vg_synset_ids = exploration.vg_synset()
    vg_synset_ids = list(set(vg_synset_ids))
    with open('VisualGenome_REFORMAT.txt', 'w') as f:
        for item in vg_synset_ids:
            f.write("%s\n" % item.split('.')[0].replace('_', " "))

    intersection_yolo_vg = intersection(vg_synset_ids, exploration.yolo_synset_names)
    intersection_yolo_vg.sort()
    logger.info(intersection_yolo_vg)
    with open('VG_YOLO_intersection.txt', 'w') as f:
        for item in intersection_yolo_vg:
            f.write("%s\n" % item.split('.')[0].replace('_', " "))

    logger.info(f'Yolo size: {len(exploration.yolo_synset_names)}')
    logger.info(f'VG size: {len(vg_synset_ids)}')

    three_way_intersection = intersection(vg_synset_ids, intersection_yolo_imagenet)
    logger.info(f'3-way intersection size: {len(three_way_intersection)}')

    blcs = exploration.blcs()

    logger.info(f'Number of blcs: {len(blcs)}')
    three_way_intersection_blc = intersection(three_way_intersection, blcs)
    logger.info(f'Intersection BLC and 3-way intersection: {len(three_way_intersection_blc)}')
    with open('BLC_YOLO_VisualGenome_intersection.txt', 'w') as f:
        for item in three_way_intersection_blc:
            f.write("%s\n" % item.split('.')[0].replace('_', " "))

    yolo_blc_intersection = intersection(exploration.yolo_synset_names, blcs)
    logger.info(f'Intersection BLC and yolo: {len(yolo_blc_intersection)}')
    with open('BLC_YOLO_intesection.txt', 'w') as f:
        for item in yolo_blc_intersection:
            f.write("%s\n" % item.split('.')[0].replace('_', " "))

    vg_blc_intersection = intersection(exploration.vg_synset_names, blcs)
    logger.info(f'Intersection BLC and vg: {len(vg_blc_intersection)}')
    with open('BLC_VisualGenome_intesection.txt', 'w') as f:
        for item in vg_blc_intersection:
            f.write("%s\n" % item.split('.')[0].replace('_', " "))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise

