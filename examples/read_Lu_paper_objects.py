import scipy.io as sio

matfile = sio.loadmat('data/Lu_visual_relationship_detection_objects.mat')
objects = matfile['objectListN']
objects = objects[0]
objects = [object[0] for object in objects]
print(objects)
