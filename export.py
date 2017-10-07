#!/usr/bin/env python3
''' Pull images for an Anki text export into a folder '''

import argparse
import os
import re
import shutil


def parseArgs():
    parser = argparse.ArgumentParser(
        description="""Pull images for an Anki text export into a folder.
        Example:
        python path/to/text/filename path/to/export/location""")
    parser.add_argument(
        'filename',
        help="Name of Anki text export file")
    parser.add_argument(
        'export_location',
        help="Name of folder to export images to")
    parser.add_argument(
        '--img-src-dir',
        dest='mediaDir',
        default='~/.local/share/Anki2/User 1/collection.media',
        help='Path to directory containing Anki images')
    return parser.parse_args()

def strip_img_tag_from_match_group(match_group):
    ''' Takes a regex match_group and
    returns the string pointing to the img src '''
    return match_group[6:-1]

def pullImages(inFile):
    '''
    :inFile: file to read
    Finds all image source strings
    :return: a list of image source strings
    '''
    with open(inFile) as f:
        fileRaw = f.read()

    img_src_pattern = re.compile('src="".+?"')
    images = []

    for match in re.finditer(img_src_pattern, fileRaw):
        images.append(strip_img_tag_from_match_group(match.group()))

    return images

def storeImages(images, folder, mediaDir):
  '''
  Get each image in the list of images and store it in the specified
  folder
  '''

  # Create directory
  try:
    os.mkdir(folder)
  except OSError as exception:
    # TODO check if folder is empty and continue if it is
    raise exception

  # Copy images into directory
  for img in images:
    fullPath = os.path.expanduser(os.path.join(mediaDir, img))
    if (os.path.isfile(fullPath)):
      shutil.copy(fullPath, folder)
    else:
      print("Error: file " + fullPath + " not found.")


if __name__ == '__main__':
  args = parseArgs()
  images = pullImages(args.filename)
  storeImages(images, args.export_location, args.mediaDir)
