# Datasets

We'll use this repository to:

1. Show the user how to get the data.
2. Suggest a folder structure that will work well with the remaining modules, and automate its creation.
3. Keep track of data-related issues.

## Getting the data

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
