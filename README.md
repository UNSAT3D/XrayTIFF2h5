# Datasets

We'll use this repository to:

1. Show the user how to get the data.
2. Suggest a folder structure that will work well with the remaining modules, and automate its creation.
3. Keep track of data-related issues.

## The published data

### Using `make`

1. Copy or clone this repository in the location you want to store your local copy of the data.
2. Open a console.
3. Run `make`.

### Using `snakemake`

1. Copy or clone this repository in the location you want to store your local copy of the data.
2. Open a console.
3. Run `snakemake -j 1`.

### Manually

1. Copy or clone this repository in the location you want to store your local copy of the data.
2. Save the dataset [X-ray Computed Tomography Reconstructions of Partially Saturated Vegetated Sand](https://doi.org/10.4121/21294510.v2) inside the `exp` folder. Uncompress if necessary.
3. Save the dataset [Phase field data generated from coupled Lattice Boltzmann-discrete element simulations](https://doi.org/10.4121/21272874.v1) inside the `sim` folder. Uncompress if necessary.

The resulting working folder should look like:

```bash
.
├── exp
│   ├── CoarseSand_Day2Growth.tif
│   ├── CoarseSand_Day6Growth.tif
│   ├── FineSand_Day2Growth.tif
│   ├── FineSand_Day6Growth.tif
│   └── README.txt
└── sim
    ├── colour_output_t00250000-0285621391.h5
    ├── particle_configuration.dat
    └── README.md
```

## The full dataset

The full dataset is, for now, only available on surfdrive.
The format for the x-ray data is:

```bash
data
├── coarse
│   └───── loose
│   │       └──── sample_id
│   │               └──── day-01.tif
│   │               └──── day-02.tif
│   │               └──── ...
│   └──── dense
│           └──── sample_id
│           └──── ...
└── fine
│   └──── loose
│   │       └──── sample_id
│   │       └──── ...
    └──── dense
│           └──── sample_id
│           └──── ..
```

and the format for the labels is identical.

Running the following
```bash
python tif_to_h5.py --data_path data --label_path labels --h5_path data.h5
```
will combine all the tif files into a single .h5 file, following again the same structure,
except that now for each sample we have:
```bash
sample_id
├── data (num_days, 1600, 650, 650), float16
└── labels (num_days, 1600, 650, 650), float16
```

It also changes the class labels to:
- 0: water
- 1: outside of bounds of sample
- 2: air
- 3: root
- 4: soil
