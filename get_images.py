"""
Download images from internet to train your model
"""
from os import PathLike

from raduw_utils import save_image, remove_bad_images, ensure_dir
from pathlib import Path
from duckduckgo_search import DDGS
import shutil

cleanup = True

def main():
    image_dir = Path("./my-images")
    if cleanup:
        shutil.rmtree(image_dir, ignore_errors=True)
        image_dir.mkdir(parents=True, exist_ok=True)
    download_bear_images(image_dir)


def download_bear_images(image_dir: PathLike):
    idx = 1
    bear_dir = Path(image_dir) / f"bears"
    bear_types = ['grizzly', 'black', 'teddy']
    with DDGS() as ddgs:
        for query in bear_types:
            results = []
            for result in ddgs.images(f"{query} bear", max_results=150):
                url = result['image']
                dir = bear_dir / query
                if save_image(url, dir, query, idx=idx):
                    idx += 1
                else:
                    print(f"failed to save image {result}")


if __name__ == '__main__':
    main()
