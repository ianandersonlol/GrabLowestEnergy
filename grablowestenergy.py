import argparse
import os
import shutil
from pathlib import Path

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Process Rosetta score and PDB files.")
    parser.add_argument("-i", "--input-dir", type=str, help="Input directory.")
    parser.add_argument("-o", "--output-dir", type=str, help="Output directory.")
    parser.add_argument("-n", "--hit-length", type=int, default=5, help="Number of hits to select (default: 5).")
    return parser.parse_args()


def main():
    args = parse_args()
    print(args)

    input_dir = Path(args.input_dir) if args.input_dir else Path.cwd()
    output_dir = Path(args.output_dir) if args.output_dir else input_dir

    if not input_dir.exists():
        print(f"Input directory {input_dir} does not exist.")
        return

    if not output_dir.exists():
        print(f"Output directory {output_dir} does not exist, creating...")
        output_dir.mkdir(parents=True)

    for protein_dir in input_dir.iterdir():
        if not protein_dir.is_dir():
            continue

        protein_name = protein_dir.name
        print(f"Processing {protein_name}...")

        results_dir = protein_dir / "results"
        if not results_dir.exists():
            print(f"Results directory {results_dir} does not exist, skipping.")
            continue

        score_files = list(results_dir.glob("*.sc"))
        pdb_files = list(results_dir.glob("*.pdb"))

        if len(score_files) == 0:
            print(f"No score files found in {protein_name}.")
            continue

        protein_output_folder = output_dir / protein_name
        protein_output_folder.mkdir(exist_ok=True)

        output_scores_path = protein_output_folder / f"{protein_name}_scores.csv"

        dfs = []

        for score_file in score_files:
            print(f"Processing score file {score_file}...")
            df = pd.read_csv(score_file, sep="\s+", header=1)

            if "SCORE:" in df.columns:
                del df["SCORE:"]

            if df.empty:
                print(f"DataFrame is empty for score file {score_file}.")
                continue

            dfs.append(df)

        combined_df = pd.concat(dfs, ignore_index=True)

        if "description" in combined_df.columns:
            combined_df = combined_df.drop_duplicates(subset="description", keep="last")
            sorted_df = combined_df.sort_values("total_score")
            low_energy_pdbs = [f"{pdb_name}.pdb" for pdb_name in sorted_df["description"].head(args.hit_length).to_list()]
        else:
            low_energy_pdbs = combined_df["pdbfile"].head(args.hit_length).to_list()

        cleaned_low_energy_pdbs = []
        for pdb_name in low_energy_pdbs:
            pdb_file = next((p for p in pdb_files if os.path.basename(p) == pdb_name), None)
            if pdb_file is None:
                print(f"Could not find PDB file for {pdb_name} in score file {score_file}.")
                continue

            output_file = protein_output_folder / pdb_file.name
            if output_file.is_file():
                print(f"Output file {output_file} already exists, skipping.")
                continue

            shutil.copy2(pdb_file, output_file)
            print(f"Copied {pdb_file} to {output_file}")
            cleaned_low_energy_pdbs.append(pdb_file.stem)

        if len(cleaned_low_energy_pdbs) > 0:
            with open(output_scores_path, "w") as f:
                f.write("\n".join(cleaned_low_energy_pdbs))


if __name__ == "__main__":
    main()