import os
import subprocess
from typing import List, Tuple
from Bio import Entrez, SeqIO

# Set your email for NCBI Entrez
Entrez.email = "your.email@example.com"

# ----------------------------
# 1. Fetch Protein Sequences
# ----------------------------


def fetch_protein_sequences(queries: List[Tuple[str, str]], out_dir: str) -> List[str]:
    os.makedirs(out_dir, exist_ok=True)
    fasta_paths = []
    for gene, org in queries:
        query = f"{gene}[Gene Name] AND {org}[Organism] AND srcdb_refseq[PROP]"
        print(f"Fetching: {query}")
        try:
            handle = Entrez.esearch(db="protein", term=query, retmax=1)
            record = Entrez.read(handle)
            ids = record["IdList"]
            if not ids:
                print(f"  ❌ No hit found for {gene} in {org}")
                continue

            fetch_handle = Entrez.efetch(
                db="protein", id=ids[0], rettype="fasta", retmode="text"
            )
            seq_record = SeqIO.read(fetch_handle, "fasta")
            file_path = os.path.join(out_dir, f"{org.replace(' ', '_')}.fasta")
            SeqIO.write(seq_record, file_path, "fasta")
            fasta_paths.append(file_path)
            print(f"  ✅ Saved to {file_path}")
        except Exception as e:
            print(f"  ⚠️ Error fetching {org}: {e}")
    return fasta_paths


# ----------------------------
# 2. Align Sequences
# ----------------------------


def run_alignment(input_files: List[str], method: str = "mafft") -> str:
    combined_input = "combined.fasta"
    with open(combined_input, "w") as out:
        for path in input_files:
            with open(path) as f:
                out.write(f.read())

    output_file = f"alignment_{method}.fasta"

    if method == "mafft":
        cmd = ["mafft", "--auto", combined_input]
    elif method == "clustalo":
        cmd = ["clustalo", "-i", combined_input, "-o", output_file, "--force"]
    elif method == "muscle":
        cmd = ["muscle", "-in", combined_input, "-out", output_file]
    else:
        raise ValueError("Invalid alignment method")

    print(f"Running alignment with {method}...")
    if method == "mafft":
        with open(output_file, "w") as f:
            subprocess.run(cmd, stdout=f, check=True)
    else:
        subprocess.run(cmd, check=True)

    print(f"  ✅ Alignment written to {output_file}")
    return output_file


# ----------------------------
# 3. Build Phylogenetic Trees
# ----------------------------


def run_fasttree(alignment_file: str) -> str:
    output_tree = alignment_file.replace(".fasta", ".fasttree.nwk")
    cmd = ["FastTree", "-lg", alignment_file]
    print("Building FastTree...")
    with open(output_tree, "w") as out:
        subprocess.run(cmd, stdout=out, check=True)
    print(f"  ✅ Tree saved to {output_tree}")
    return output_tree


def run_raxml(alignment_file: str) -> str:
    base = alignment_file.replace(".fasta", "")
    print("Building RAxML tree...")
    cmd = [
        "raxmlHPC-PTHREADS",
        "-T",
        "2",
        "-s",
        alignment_file,
        "-n",
        "raxml_tree",
        "-m",
        "PROTGAMMAJTT",
        "-p",
        "12345",
        "-#",
        "100",
    ]
    subprocess.run(cmd, check=True)
    output = "RAxML_bestTree.raxml_tree"
    print(f"  ✅ Tree saved to {output}")
    return output


def run_iqtree(alignment_file: str) -> str:
    print("Building IQ-TREE tree...")
    cmd = [
        "iqtree",
        "-s",
        alignment_file,
        "-m",
        "MFP",
        "-B",
        "1000",
        "--prefix",
        "iqtree_out",
    ]
    subprocess.run(cmd, check=True)
    output = "iqtree_out.treefile"
    print(f"  ✅ Tree saved to {output}")
    return output


# ----------------------------
# 4. Main
# ----------------------------

if __name__ == "__main__":
    species = [
        ("fliC", "Escherichia coli"),
        ("fliC", "Pseudomonas aeruginosa"),
        ("flaB", "Borrelia burgdorferi"),
        ("fliC", "Serratia marcescens"),
        ("fliC", "Shewanella oneidensis"),
        ("flaA", "Vibrio cholerae"),
        ("fliM", "Listeria monocytogenes"),
        ("fliC", "Salmonella enterica"),
        ("flaA", "Agrobacterium tumefaciens"),
        ("fliC", "Clostridioides difficile"),
    ]

    # Step 1: Fetch
    print("\n🔎 Fetching protein sequences...")
    fasta_files = fetch_protein_sequences(species, out_dir="fasta_seqs")

    # Step 2: Align
    print("\n🔗 Running alignment...")
    msa_file = run_alignment(fasta_files, method="mafft")

    # Step 3: Build trees
    print("\n🌳 Building phylogenetic trees...")
    fasttree_out = run_fasttree(msa_file)
    raxml_out = run_raxml(msa_file)
    iqtree_out = run_iqtree(msa_file)

    print("\n✅ Workflow complete.")
    print("Output trees:")
    print(f"  - FastTree: {fasttree_out}")
    print(f"  - RAxML:    {raxml_out}")
    print(f"  - IQ-TREE:  {iqtree_out}")
