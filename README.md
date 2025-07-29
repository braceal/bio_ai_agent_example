# Bio AI Agent Example

A Python application for automated phylogenetic analysis using local bioinformatics tools. This workflow fetches protein sequences directly from NCBI, performs multiple sequence alignment, and builds phylogenetic trees.

## Overview

This workflow performs comparative analysis of flagellin proteins across different bacterial species:

1. **Sequence Retrieval**: Fetches protein sequences from NCBI using Biopython
2. **Multiple Sequence Alignment**: Aligns sequences using MAFFT, ClustalO, or MUSCLE
3. **Phylogenetic Analysis**: Builds trees using FastTree, RAxML, and IQ-TREE
4. **Output**: Generates publication-ready phylogenetic trees in Newick format

## Prerequisites

### Python Requirements
- Python 3.8 or higher
- Internet connection for NCBI database queries

### External Bioinformatics Tools

You'll need to install the following command-line tools (install instructions below):

**Alignment Tools:**
- [MAFFT](https://mafft.cbrc.jp/alignment/software/) - Multiple sequence alignment
- [Clustal Omega](http://www.clustal.org/omega/) - Multiple sequence alignment
- [MUSCLE](https://drive5.com/muscle/) - Multiple sequence alignment

**Phylogenetic Tools:**
- [FastTree](http://www.microbesonline.org/fasttree/) - Fast phylogenetic tree construction
- [RAxML](https://cme.h-its.org/exelixis/web/software/raxml/) - Maximum likelihood phylogenetic analysis
- [IQ-TREE](http://www.iqtree.org/) - Efficient phylogenetic inference

## Setup Instructions

### 1. Clone the Repository

```bash
git clone git@github.com:braceal/bio_ai_agent_example.git
cd bio_ai_agent_example
```

### 2. Create a Virtual Environment

Create and activate a Python virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Python Dependencies

Install the required Python packages:

```bash
conda create -n bio_ai_agent_example python=3.12
conda activate bio_ai_agent_example
pip install biopython
conda install -c bioconda mafft clustalo muscle fasttree raxml iqtree -y
```

### 4. Configure Email for NCBI

Edit `workflow.py` and update the email address for NCBI Entrez queries:

```python
Entrez.email = "your.email@example.com"  # Replace with your actual email
```

**Note**: The code runs without changing the email address.

## Usage

Run the complete phylogenetic analysis workflow:

```bash
python workflow.py
```

### What the workflow does:

1. **Fetches protein sequences** for flagellin genes from 10 bacterial species
2. **Creates individual FASTA files** in the `fasta_seqs/` directory
3. **Combines and aligns sequences** using MAFFT
4. **Builds three phylogenetic trees** using different methods:
   - FastTree (fast approximate method)
   - RAxML (maximum likelihood with bootstrap)
   - IQ-TREE (model selection + ultrafast bootstrap)

### Output Files

The workflow generates several output files:

- `fasta_seqs/` - Directory containing individual FASTA files for each species
- `combined.fasta` - All sequences combined into one file
- `alignment_mafft.fasta` - Multiple sequence alignment
- `alignment_mafft.fasttree.nwk` - FastTree phylogeny
- `RAxML_bestTree.raxml_tree` - RAxML phylogeny
- `iqtree_out.treefile` - IQ-TREE phylogeny

## Customization

### Modify Species List

Edit the `species` list in `workflow.py` to analyze different genes/organisms:

```python
species = [
    ("gene_name", "Organism name"),
    ("fliC", "Escherichia coli"),
    # Add more species...
]
```

### Change Alignment Method

Modify the alignment method call:

```python
msa_file = run_alignment(fasta_files, method="clustalo")  # or "muscle"
```

### Select Different Tree Methods

Comment out tree-building methods you don't need:

```python
# fasttree_out = run_fasttree(msa_file)  # Skip FastTree
raxml_out = run_raxml(msa_file)           # Keep RAxML
iqtree_out = run_iqtree(msa_file)         # Keep IQ-TREE
```

## Project Structure

- `workflow.py` - Main phylogenetic analysis workflow
- `requirements.txt` - Python dependencies
- `README.md` - This documentation
- `fasta_seqs/` - Output directory for individual sequences (created during run)

## Deactivating the Virtual Environment

When finished, deactivate the virtual environment:

```bash
deactivate
```