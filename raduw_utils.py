from io import BytesIO
from typing import List
import pathlib
from pathlib import Path
from os import PathLike
import requests
from PIL import Image


def ensure_dir(path: PathLike) -> None:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)

def save_image(url: str, dir_path: PathLike, prefix, idx: int ) -> bool:

    # download image
    try:
        r = requests.get(url)
    except:
        print(f"failed to retrieve image {url}")
        return False

    # test that the content is a valid image we can work with
    try:
        img = Image.open(BytesIO(r.content))
    except:
        print("Could not open the image")
        return False

    # save it to file
    file_name = url
    try:
        ensure_dir(dir_path)
        file_name = _get_file_name(url, dir_path, prefix, idx, default_extension=".jpg")
        img.save(file_name)
    except Exception as e:
        print(f"failed to save image {file_name.absolute()}")
        return False

    return True


def _get_file_name(url: str, directory: PathLike, name_prefix: str, index: int = 1, default_extension=None) -> Path:
    p = pathlib.Path(url)
    stem = p.stem
    suffix = p.suffix

    if not suffix and default_extension:
        suffix = default_extension
    # create name
    name = Path(f"{name_prefix}-{index}").with_suffix(suffix)
    p = directory / name
    if not Path.exists(p):
        return p
    raise Exception(f"File '{name}' already exists")


def remove_bad_images(image_dir: PathLike):
    for file in Path(image_dir).glob("*.jpg"):
        try:
            im = Image.open(file)
        except Exception as ex:
            print(f"Removing bad image {file}, error: {ex}")
            file.unlink()
