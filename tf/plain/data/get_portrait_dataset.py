from PIL import Image
import time
import os
import imageio
import numpy as np
import csv

def save_dataset_to_csv(dataset, artistName=None):

    print("writing outfile", flush=True)

    outFileName = "./{}.csv".format(artistName)

    with open(outFileName, 'w') as f:

        writer = csv.writer(f, delimiter=',')
        for i in range(dataset.shape[0]):

            writer.writerow(dataset[i].tolist())

def get_image_encoding(imageName):

    data = None 

    with Image.open(imageName) as img:

        img = img.resize((256,256))

        if img.mode == "L":
            print("grayscale image:", img.mode)
            return None 

        shape = img.size + (3,)

        data = np.array(list(img.getdata()))
        data = data.reshape(shape)
        data = (data - 127.5) / 127.5

    return data

def get_portrait_dataset(portraitFolder, images):

    print("reading portrait dataset...", flush=True)
    dataset = []

    for imageName in images:

        imageName = os.path.join(portraitFolder, imageName)
        data = get_image_encoding(imageName)

        if data is not None:
            dataset.append(data)

    dataset = np.array(dataset)

    save_dataset_to_csv(dataset, 'portrait faces')

    return dataset

def get_artist_dataset(artistFolder, images):

    print("reading " + artistFolder, flush=True)
    dataset = []

    for imageName in images:

        imageName = os.path.join(artistFolder, imageName)
        data = get_image_encoding(imageName)
        if data is not None:
            dataset.append(data)

    return np.array(dataset)

def extract_artist(artist, imagesDir):

    artistFolder = os.path.join(imagesDir, artist)
    images = os.listdir(artistFolder)

    dataset = get_artist_dataset(artistFolder, images)

    print(artistFolder)
    artistName = os.path.basename(artistFolder)
    print(artistName, flush=True)
    save_dataset_to_csv(dataset, artistName)
    
def extract_image_data():

    imagesDir = "../data/images/images/"
    artists = os.listdir(imagesDir)

    for artist in artists:

        extract_artist(artist, imagesDir)
        
portraitDir = './datasets/portrait_faces/'
portraits = os.listdir(portraitDir)
get_portrait_dataset(portraitDir, portraits)
