import h5py
import numpy as np
import argparse

def convert_labels_chunk(chunk):
    binary_labels = np.where(chunk == 3, 1, 0)  # Root is 1, all else is 0
    return binary_labels

def process_h5_file_in_chunks(input_file, chunk_size=10):
    with h5py.File(input_file, 'r+') as f:
        crops = list(f.keys())
        for crop in crops:
            print(f"Processing crop: {crop}")
            for level in f[crop].keys():
                print(f"  Processing level: {level}")
                for structure in f[crop][level].keys():
                    print(f"    Processing structure: {structure}")
                    for dataset in f[crop][level][structure].keys():
                        if 'labels' in dataset:
                            print(f"      Processing dataset: {dataset}")
                            labels_dataset = f[crop][level][structure][dataset]
                            shape = labels_dataset.shape
                            num_samples = shape[0]
                            height = shape[1]
                            width = shape[2]

                            # Process dataset in smaller chunks
                            for i in range(0, num_samples, chunk_size):
                                for j in range(0, height, chunk_size):
                                    i_end = min(i + chunk_size, num_samples)
                                    j_end = min(j + chunk_size, height)

                                    chunk = labels_dataset[i:i_end, j:j_end, :, :]
                                    print(f"        Converting chunk ({i}:{i_end}, {j}:{j_end}, : , : ) to binary")
                                    binary_chunk = convert_labels_chunk(chunk)
                                    labels_dataset[i:i_end, j:j_end, :, :] = binary_chunk

                            print(f"      Finished processing dataset: {dataset}")
                    print(f"    Finished processing structure: {structure}")
                print(f"  Finished processing level: {level}")
            print(f"Finished processing crop: {crop}")

def main():
    parser = argparse.ArgumentParser(description='Process HDF5 file for binary classification.')
    parser.add_argument('input_file', type=str, help='Path to the input HDF5 file')
    parser.add_argument('--chunk_size', type=int, default=10, help='Chunk size for processing large datasets')

    args = parser.parse_args()

    process_h5_file_in_chunks(args.input_file, args.chunk_size)

if __name__ == '__main__':
    main()

