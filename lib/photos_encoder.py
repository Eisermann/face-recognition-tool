import logging
import os
import typing

import face_recognition
from numpy.core.records import ndarray

LOGGER = logging.getLogger(__file__)


class PhotosEncoder:

    def __init__(self, photos_directory):
        self.photos_directory = photos_directory

    def load_photos(self) -> (typing.List[int], typing.List[ndarray]):
        photos = os.listdir(self.photos_directory)

        encodings = []
        ids = []

        for photo_file_name in photos:
            try:
                file = self._load_photo(photo_file_name)
            except OSError:
                LOGGER.error(f"Cannot load file: {photo_file_name}")
                continue

            encoding = self._get_face_encoding(file)

            if encoding is not None:
                ids.append(self._extract_photo_id(photo_file_name))
                encodings.append(encoding)

        return ids, encodings

    def _load_photo(self, file_name: str) -> ndarray:
        LOGGER.info(f"Loading file: {file_name}")

        file_path = os.path.join(self.photos_directory, file_name)

        return face_recognition.load_image_file(file_path)

    @staticmethod
    def _get_face_encoding(file: ndarray) -> ndarray:
        encodings = face_recognition.face_encodings(file)

        if len(encodings) == 1:
            return encodings[0]
        elif len(encodings) > 1:
            LOGGER.error(f"Photo contains more than one face.")
        else:
            LOGGER.error(f"Photo does not contain a face.")

    @staticmethod
    def _extract_photo_id(file_name: str) -> int:
        return int(file_name.split('.')[0])
