import nltk
from size_comparisons.exploration.compare_synset_lists import SynsetsExploration, intersection

from size_comparisons.parse_objects import InputsParser
from size_comparisons.scraping.analyze import analyze_results

nltk.download('wordnet')


# TODO: think about 3-grams (body of water)

def main(analyze_blc_intersection=False):
    """Compile dataframe with scraper data and plot some results."""
    inputparser = InputsParser()
    labels = inputparser.retrieve_labels()
    names = inputparser.retrieve_names()


    analyze_results(labels, names)

    if analyze_blc_intersection:
        exploration = SynsetsExploration(InputsParser())
        exploration.retrieve_reformat_lists()

        yolo_blc = intersection(exploration.yolo_synset_names, exploration.blc_synset_names)
        index_yolo_in_blc = [name in yolo_blc for name in exploration.yolo_synset_names]
        selected_names = list()
        yolo_blc_ids = list()
        for i, label in enumerate(labels):
            if index_yolo_in_blc[i]:
                yolo_blc_ids.append(label)
                selected_names.append(names[i])
                if label == 'n04088797':
                    print(names[i])

        analyze_results(yolo_blc_ids, selected_names)




if __name__ == "__main__":
    main()
