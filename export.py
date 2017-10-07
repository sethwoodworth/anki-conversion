#!/usr/bin/env python3
''' Pull images for an Anki text export into a folder '''

import argparse
import os
import re
import shutil

class MediaList(list):
    ''' Handles and copies media from Anki decks '''

    def __init__(self, media_source, media_destination, exported_deck_file):
        self.media_source = media_source
        self.media_destination = media_destination
        self.exported_deck_file = exported_deck_file

        self._parse_exported_deck_file()


    def _parse_exported_deck_file(self):
        # Finds all image source strings
        with open(self.exported_deck_file) as f:
            file_raw = f.read()

        img_src_pattern = re.compile('src="".+?"')

        for match in re.finditer(img_src_pattern, file_raw):
            self.append(
                self._strip_img_tag_from_match_group(match.group())
            )

    def _strip_img_tag_from_match_group(self, match_group):
        ''' Takes a regex match_group and
        returns the string pointing to the img src '''
        return match_group[6:-1]


    def copy_media(self):

      # Create directory
      try:
        os.mkdir(self.media_destination)
      except OSError as exception:
        # TODO check if folder is empty and continue if it is
        raise exception

      # Copy images into directory
      for img in self:
        source_path = os.path.expanduser(os.path.join(self.media_source, img))
        if os.path.isfile(source_path):
          shutil.copy(source_path, self.media_destination)
        else:
          print("Error: file %s not found." % source_path)


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


if __name__ == '__main__':
  args = parseArgs()

  ml = MediaList(media_source=args.mediaDir, media_destination=args.export_location, exported_deck_file=args.filename)
  ml.copy_media()
