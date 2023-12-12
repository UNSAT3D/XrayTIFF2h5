import os
from typing import Callable

import click
import h5py
import numpy as np
import tifffile
import tqdm


DATA_MAX = 65535

def tif_to_numpy(tif_file: str, label: bool) -> np.ndarray:
    """
    Convert tif file containing a 3D scan to a numpy array.
    """
    with tifffile.TiffFile(tif_file) as tif:
        images = tif.asarray()
        images = np.expand_dims(images, axis=-1)

    if not label:
        images = images.astype(np.float32)
        images = images / DATA_MAX
        images = images.astype(np.float16)
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
            for day in tqdm.tqdm(sorted(files)):
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
    Convert the labels according to:
        0   -> 0: Pixels referring to water
        1   -> 1: Outside the soil sample
        85  -> 2: Pixels referring to air
        128 -> 3: Pixels referring to the root system
        255 -> 4: Pixels referring to soil grains

    Before the conversion above, convert the "mixed" labels as:
        2 -> 1
        86, 87 -> 85
        127, 129 -> 128
        212, 213, 214 -> 255
    """
    value_map = {0: 0, 1: 1, 85: 2, 128: 3, 255: 4}
    value_map_mixed = {
        2: 1,
        86: 85,
        87: 85,
        127: 128,
        129: 128,
        212: 255,
        213: 255,
        214: 255,
    }
    value_map = {k: value_map[v] for k, v in value_map_mixed.items()} | value_map

    converted_array = np.copy(array)
    for k, v in value_map.items():
        converted_array[array==k] = v

    unique_results = set(np.unique(converted_array).tolist())
    if unique_results - {0, 1, 2, 3, 4} != set():
        raise ValueError(f"Labels are not correctly converted, found {unique_results}")

    return converted_array


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
