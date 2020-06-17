# thesis_scraper
## Installation
Run `pip install -e .` in the root folder. This installs an editable package, which will automatically update when source files are modified.

## Run
Examples of the package usage are shown in the `examples` folder. The filenames explain what the file does and further information is in the comments.
 
 # Wikipedia retrieval notes
 get all images and info(but no description). see here for available properties: https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bimageinfo
https://en.wikipedia.org/w/api.php?action=query&generator=images&titles=apple&prop=imageinfo&iiprop=url&format=json&formatversion=2

Alternative in two steps:
1. get images list: https://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&format=json&prop=images
2. Get image info for one image:
https://en.wikipedia.org/w/api.php?action=query&titles=File:Malus_domestica_-_Köhler–s_Medizinal-Pflanzen-108.jpg&prop=imageinfo&iilimit=50&iiprop=timestamp|user|url
