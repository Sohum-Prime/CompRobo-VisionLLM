import cv2
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

def confirm_matching_shapes(directory):
    proper_cv2_images = [] # store the images in a list so I can persist their cv2.imread() features
    for i in os.listdir(directory):
        a = os.path.join(directory, i)
        d = cv2.imread(a)
        proper_cv2_images.append(d)
    return proper_cv2_images # want to return the np.array of all the objects in this directory, 1 (d just returns last in loop, need to use list to persist and save all images)

def preprocess_images(images):
    # convert to grayscale since we don't care too much about features
    # use two different lists to append specific items
    features = []
    labels = []
    for i, image in enumerate(images): # why does this star over as image 0 each time? 
        grayScale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        t_lower = 50 # test
        t_upper = 150 # test
        edges = cv2.Canny(grayScale, t_lower, t_upper) 
        features.append(edges.flatten()) # this creates a 1D array from edges which is useful because ...
        labels.append(f'image {i}')

    return features, labels

def process_test_images(image_paths): 
    test_features = [] 
    test_labels = []
    # loop through the image paths passed into the function
    for i, image_path in enumerate(image_paths):
        image = cv2.imread(image_path)

        if image is not None:
            single_image_features, single_image_label = preprocess_images([image])
            test_features.extend(single_image_features)
            test_labels.extend(single_image_label)
        else:
            print(f'Image at {image_path} and {i} cannot be read. ')

    # we unpack the two return values from the preprocess_images function here, so we can store their values and return them for later
    return test_features, test_labels

  
def knn(images):
    # we unpack by doing params from function, variable to assign -> I'm doing this because when I scroll on t I see tuple[list, list] and these are features, labels from the value being passed into knn function
    features, labels = t
    test_features, test_labels = call_process_test_images
    print(test_features)
    X = np.array(features)
    y = np.array(labels)
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X, y)

    for idx, test_feature in enumerate(test_features):
        test_feature_reshaped = test_feature.reshape(1, -1)
        most_similar_image_label = knn.predict(test_feature_reshaped)
        print(f"Predicted: {most_similar_image_label}, True: {test_labels[idx]}")

# Function calling
directory = '/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/featureExtraction/images/train'
call_confirm_matching_shapes = confirm_matching_shapes(directory)
t = preprocess_images(call_confirm_matching_shapes)
new_image_paths = ['/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/featureExtraction/images/test/IMG_3727.JPG', '/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/featureExtraction/images/test/IMG_3728.JPG', '/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/featureExtraction/images/test/IMG_3729.JPG', '/Users/zaynpatel/vision/visionLLM/CompRobo-VisionLLM/featureExtraction/images/test/IMG_3730.JPG']
call_process_test_images = process_test_images(new_image_paths)
c = knn(t) 
print(c)