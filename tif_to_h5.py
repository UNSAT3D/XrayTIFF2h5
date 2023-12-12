import os
from typing import Callable

import click
import h5py
import numpy as np
import tifffile
import tqdm


DATA_MAX = 65535
CLASS_VALUES = [0, 1, 85, 128, 255]


def tif_to_numpy(tif_file: str, label: bool) -> np.ndarray:
    """
    Convert tif file containing a 3D scan to a numpy array.
    """
    with tifffile.TiffFile(tif_file) as tif:
        images = tif.asarray()

    if not label:
        images = images.astype(np.float32)
        images = images / DATA_MAX
        images = images.astype(np.float16)
        images = np.expand_dims(images, axis=-1)
    else:
        images = images.astype(np.uint8)

    return images


def tifs_to_h5(path: str, f: h5py.File, label: bool = False):
    """
    Convert all tif files in a directory to a single h5 file.
    """
    for root, dirs, files in os.walk(path):
        group_path = os.path.relpath(root, path)
        if group_path == ".":
            group = f
        else:
            group = f.require_group(group_path.replace(os.sep, "/"))

        # if we are at a leaf
        if not dirs and files:
            print(f"Converting {root} to h5")
            data_days = []
            files_per_day = sorted(files)
            for day in tqdm.tqdm(files_per_day):
                if not day.endswith(".tif"):
                    continue

                data = tif_to_numpy(os.path.join(root, day), label)
                if label:
                    data = convert_labels(data)
                data_days.append(data)
            data_days = np.stack(data_days, axis=0)

            group.create_dataset("labels" if label else "data", data=data_days)


def convert_labels(array: np.ndarray) -> np.ndarray:
    """
    Convert the labels to the nearest class value, then convert the labels according to:
        0   -> 0: Pixels referring to water
        1   -> 1: Outside the soil sample
        85  -> 2: Pixels referring to air
        128 -> 3: Pixels referring to the root system
        255 -> 4: Pixels referring to soil
    """
    class_values = np.array(CLASS_VALUES).reshape(1, -1)
    diffs = np.abs(array.reshape(-1, 1) - class_values)

    # this already gives indices into CLASS_VALUES, so we can use it directly
    nearest_class = np.argmin(diffs, axis=1)
    nearest_class = nearest_class.reshape(array.shape)

    return nearest_class


@click.command()
@click.option("--data_path", help="Path to the directory containing the tif files.")
@click.option("--label_path", help="Path to the directory containing the tif files.")
@click.option("--h5_path", help="Path to the h5 file to be created.")
def main(data_path: str, label_path: str, h5_path: str) -> None:
    with h5py.File(h5_path, "w") as f:
        tifs_to_h5(label_path, f, convert_labels)
        tifs_to_h5(data_path, f)


if __name__ == "__main__":
    main()
