# grablowestenergy Documentation

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Arguments](#arguments)
- [Output](#output)
- [Examples](#examples)

## Overview

The `grablowestenergy` script processes Rosetta score and PDB files located in a specified input directory. It identifies a number of PDB files with the lowest energy scores and copies them to an output directory. This tool is especially useful for researchers working with protein structure predictions, where selecting the most stable conformations (lowest energy) is essential.

## Installation

Before using the script, ensure that you have Python installed on your system. Additionally, the `pandas` library is required for handling data operations within the script. 

To install `pandas`, run the following command:

```bash
pip install pandas
```

## Usage

To use `grablowestenergy`, navigate to the directory containing the script and run it from the command line with the appropriate arguments.

```bash
python grablowestenergy.py -i <input_dir> -o <output_dir> -n <hit_length>
```

## Arguments

| Argument         | Description                                                  | Required | Default Value |
|------------------|--------------------------------------------------------------|----------|---------------|
| `-i`, `--input-dir`  | Specify the input directory containing protein folders.      | Yes      | Current Working Directory |
| `-o`, `--output-dir` | Specify the output directory where selected PDB files are copied. | No       | Same as input directory |
| `-n`, `--hit-length` | Number of hits (low energy PDB files) to select.             | No       | 5             |

## Output

The script will process each protein folder in the input directory. It will then combine score files (`.sc`) into a single CSV file and select the specified number of PDB files with the lowest total score. These PDB files are then copied to the output directory, maintaining their original file names.

An additional file named `<protein_name>_scores.csv` will be created in each protein's output folder, listing the names of the PDB files with the lowest energy that were copied over.

## Examples

Running the script to process files in the default current working directory and select the top 5 low-energy PDB files:

```bash
python grablowestenergy.py
```

Specifying an input directory (`/path/to/input`) and using the default hit length:

```bash
python grablowestenergy.py -i /path/to/input
```

Specifying both input (`/path/to/input`) and output (`/path/to/output`) directories, along with selecting the top 10 low-energy PDB files:

```bash
python grablowestenergy.py -i /path/to/input -o /path/to/output -n 10
```

If you encounter any issues during execution, make sure the input directory contains the correct structure of protein folders, each with a `results` subfolder containing the `.sc` and `.pdb` files. The script will inform you if the necessary directories or files are missing.
Markdown documentation has been created: ('grablowestenergy', '.py').md