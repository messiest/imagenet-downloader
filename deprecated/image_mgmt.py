import os
import numpy as np
import cv2


def get_label_vectors():
    """
        generate label vectors from collected images

    :return: dictionary of labels and label vectors
    :rtype: dict
    """
    print("Retrieving label vectors...")
    label_dict = {}                                                         # instantiate dict for labels:vectors
    categories = sorted([c for c in os.listdir('images/') if c[0] != '.'])  # ignore hidden files
    x = np.zeros(len(categories))                                           # zero vector of number of categories
    for i, c in enumerate(categories):                                      # get index and category for images
        y = x.copy()                                                        # use copy of x
        y[i] = 1                                                            # set label index to true
        label_dict[c] = y.copy()                                            # create label:vector

    return label_dict


def load_image_data():
    """
        load image data from collected categories

    :param label_dict: dictionary of label:image pairs
    :type label_dict: dict
    :return: label vector, data vectors
    :rtype: numpy.ndarray
    """
    print("Loading image data...")
    label_dict = get_label_vectors()
    categories = [c for c in os.listdir('images/') if c[0] != '.']         # ignore
    labels = []                                                            # instantiate list for image labels
    data = []                                                              # instantiate list for image data
    for i in categories:
        path = 'images/{}/'.format(i)                                      # define path to category folder
        for j in os.listdir(path):                                         # get images from category folder
            labels.append(label_dict[i])                                   # append label vector
            data.append(cv2.imread(path + j).flatten())                    # append flattened image data

    labels = np.array(labels)                                              # convert lists to array
    data = np.array(data)
    print("Done.")

    return labels, data

def main():
    """
        main method of image_mgmt.py

    :return:
    :rtype:
    """
    labels, data = load_image_data()
    print(labels.shape, data.shape)


if __name__ == "__main__":
    main()
