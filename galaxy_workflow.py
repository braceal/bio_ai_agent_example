import os
from typing import List, Tuple
from bioblend.galaxy import GalaxyInstance
from dotenv import load_dotenv


def connect_to_galaxy(url: str, api_key: str) -> GalaxyInstance:
    return GalaxyInstance(url=url, key=api_key)


def fetch_protein_sequences(
    gi: GalaxyInstance, history_id: str, gene_queries: List[Tuple[str, str]]
) -> List[str]:
    """
    Fetch protein sequences for a list of gene/org pairs from NCBI.

    Returns a list of dataset IDs.
    """
    tool_id = "ncbi_esearch"
    datasets = []

    for gene, org in gene_queries:
        query = f'{gene}[gene] AND "{org}"[orgn] AND refseq[filter]'
        inputs = {"query": query, "return_type": "protein_fasta"}
        response = gi.tools.run_tool(history_id, tool_id, inputs)
        datasets.append(response["outputs"][0]["id"])

    return datasets


def merge_fasta_datasets(
    gi: GalaxyInstance, history_id: str, dataset_ids: List[str]
) -> dict:
    """
    Merge FASTA datasets into a dataset collection.
    """
    collection_description = {
        "collection_type": "list",
        "element_identifiers": [
            {"name": f"seq_{i}", "src": "hda", "id": ds_id}
            for i, ds_id in enumerate(dataset_ids)
        ],
    }

    return gi.histories.create_dataset_collection(
        history_id,
        name="merged_fasta",
        collection_type="list",
        element_identifiers=collection_description["element_identifiers"],
    )


def run_alignment(
    gi: GalaxyInstance, history_id: str, input_dataset_id: str, method: str = "mafft"
) -> dict:
    """
    Align sequences using MAFFT, MUSCLE, or Clustal Omega.
    """
    tool_map = {
        "mafft": "toolshed.g2.bx.psu.edu/repos/devteam/mafft/mafft/7.221.1",
        "clustal_omega": "toolshed.g2.bx.psu.edu/repos/devteam/clustalomega/clustalomega/1.2.0",
        "muscle": "toolshed.g2.bx.psu.edu/repos/devteam/muscle/muscle/3.8.31",
    }

    if method not in tool_map:
        raise ValueError(f"Unsupported alignment method: {method}")

    tool_id = tool_map[method]
    inputs = {"input_file": {"src": "hda", "id": input_dataset_id}}

    return gi.tools.run_tool(history_id, tool_id, inputs)


def build_tree(
    gi: GalaxyInstance, history_id: str, msa_dataset_id: str, method: str = "fasttree"
) -> dict:
    """
    Build phylogenetic tree using FastTree, RAxML, or IQ-TREE.
    """
    tool_map = {
        "fasttree": "toolshed.g2.bx.psu.edu/repos/iuc/fasttree/fasttree/2.1.10",
        "raxml": "toolshed.g2.bx.psu.edu/repos/iuc/raxml/raxml/8.2.12.1",
        "iqtree": "toolshed.g2.bx.psu.edu/repos/iuc/iqtree/iqtree/2.1.2",
    }

    if method not in tool_map:
        raise ValueError(f"Unsupported tree-building method: {method}")

    inputs = {"input": {"src": "hda", "id": msa_dataset_id}}

    if method == "raxml":
        inputs.update({"model": "PROTGAMMAJTT", "bootstrap_replicates": 100})
    elif method == "iqtree":
        inputs.update({"model": "AUTO", "ultrafast_bootstrap": 1000})
    elif method == "fasttree":
        inputs.update({"model": "JTT+CAT"})

    return gi.tools.run_tool(history_id, tool_map[method], inputs)


def export_tree_file(
    gi: GalaxyInstance,
    history_id: str,
    tree_dataset_id: str,
    filename: str = "treefile.newick",
) -> str:
    """
    Download the Newick tree file locally.
    """
    file_path = gi.datasets.download_dataset(
        dataset_id=tree_dataset_id, file_path=filename, use_default_filename=False
    )
    return file_path


if __name__ == "__main__":
    # Use dotenv to load the API key
    load_dotenv()
    api_key = os.getenv("GALAXY_API_KEY")
    if not api_key:
        raise ValueError("GALAXY_API_KEY is not set in the environment variables")

    # Setup
    gi = connect_to_galaxy("http://example.galaxy.url", api_key)

    breakpoint()

    history = gi.histories.create_history("Flagellin Analysis")

    # Example species list
    queries = [
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

    # Run
    datasets = fetch_protein_sequences(gi, history["id"], queries)
    merged = merge_fasta_datasets(gi, history["id"], datasets)
    alignment = run_alignment(gi, history["id"], merged["id"], method="mafft")
    tree = build_tree(gi, history["id"], alignment["outputs"][0]["id"], method="iqtree")
    exported_path = export_tree_file(gi, history["id"], tree["outputs"][0]["id"])
