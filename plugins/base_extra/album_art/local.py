import io
from os import path, listdir
import settings
from plugins.base.music.models import Album


def fetch_local_art(album: Album):
    """
    Finds the first matching image for an album found in
    the music library.

    Loops through each track, and checks each file in the track
    directory until one of them is a valid image file.
    :param album: The album to fetch art for
    :return: The image file binary
    """
    music_path = settings.get_key('plugins.base.music.path')

    valid_extensions = ['.jpg', '.gif', '.png', '.tga', '.bmp']
    visited_paths = []
    for track in album.tracks:
        folder = path.join(music_path, path.dirname(track.path))

        if folder in visited_paths:
            continue

        visited_paths.append(folder)
        for file in listdir(folder):
            ext = path.splitext(file)[1]
            if ext.lower() not in valid_extensions:
                continue

            img_path = path.join(folder, file)
            with open(img_path, 'rb') as f:
                return io.BytesIO(f.read())

    return None
