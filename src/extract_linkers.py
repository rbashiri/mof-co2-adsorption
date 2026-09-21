# Import pandas to expand linker lists into separate columns
import pandas as pd

# Import RDKit tools for reading SMILES and processing fragments
from rdkit import Chem

# Import the tool for disconnecting metal–ligand bonds
from rdkit.Chem.MolStandardize import rdMolStandardize


# Define the atomic numbers used to identify isolated metal atoms
metal_atomic_numbers = (
    list(range(3, 5)) +
    list(range(11, 14)) +
    list(range(19, 32)) +
    list(range(37, 51)) +
    list(range(55, 85)) +
    list(range(87, 113))
)


# Define patterns for small inorganic fragments to exclude
inorganic_blacklist = [
    Chem.MolFromSmarts("[O-2]"),              # Oxide ion
    Chem.MolFromSmarts("N#N"),                # Nitrogen gas
    Chem.MolFromSmarts("[O;H2]"),             # Water
    Chem.MolFromSmarts("[O-]S(=O)(=O)[O-]"),  # Sulfate ion
]


# Define exact standalone fragment SMILES to exclude
exact_fragment_blacklist = {
    "[Zn][Zn]",      # Zinc dimer
    "[Cu][Cu]",      # Copper dimer
    "[O]",           # Isolated neutral oxygen atom
    "[Zn+3][Zn+5]",  # Charged zinc fragment found during validation
}


# Extract candidate linkers from one chemical representation
def extract_linkers(chemical):
    """Extract candidate linkers from the chemical portion of a MOFID.

    Returns:
        linker_smiles: List of retained, sanitized fragment SMILES.
        invalid_fragments: List of rejected fragments and their errors.

    Complete extraction errors are handled by the calling loop.
    """

    # Read the chemical representation without initial sanitization
    lig_mol = Chem.MolFromSmiles(chemical, sanitize=False)

    if lig_mol is None:
        raise ValueError(
            "RDKit could not create a molecule from the chemical representation"
        )

    lig_mol.UpdatePropertyCache(strict=False)

    # Disconnect metal–ligand bonds
    disconnector = rdMolStandardize.MetalDisconnector()
    disconnected_mol = disconnector.Disconnect(lig_mol)

    # Split the structure without sanitizing the fragments yet
    fragments = Chem.GetMolFrags(
        disconnected_mol,
        asMols=True,
        sanitizeFrags=False
    )

    # Store retained linkers and fragment-level errors separately
    linker_smiles = []
    invalid_fragments = []

    for frag in fragments:

        # Remove isolated metal atoms
        if frag.GetNumAtoms() == 1:
            atom = frag.GetAtomWithIdx(0)

            if atom.GetAtomicNum() in metal_atomic_numbers:
                continue

        # Remove matching small inorganic fragments
        # Require equal heavy-atom counts to protect larger molecules
        is_inorganic = any(
            frag.HasSubstructMatch(pattern)
            and frag.GetNumHeavyAtoms() == pattern.GetNumHeavyAtoms()
            for pattern in inorganic_blacklist
        )

        if is_inorganic:
            continue

        # Convert the fragment to SMILES for exact matching
        fragment_smiles = Chem.MolToSmiles(frag)

        # Remove exact unwanted standalone fragments
        if fragment_smiles in exact_fragment_blacklist:
            continue

        # Sanitize each remaining candidate individually
        try:
            frag.UpdatePropertyCache(strict=False)
            Chem.SanitizeMol(frag)

            # Generate SMILES after sanitization
            fragment_smiles = Chem.MolToSmiles(frag)

            # Recheck the exact blacklist after sanitization
            if fragment_smiles in exact_fragment_blacklist:
                continue

            # Store the retained candidate linker
            linker_smiles.append(fragment_smiles)

        except Exception as error:
            # Record the rejected fragment and its error message
            invalid_fragments.append({
                "fragment": Chem.MolToSmiles(frag),
                "error": str(error)
            })

    return linker_smiles, invalid_fragments


# Expand existing linker lists into linker_1, linker_2, etc.
def expand_linker_columns(df_chemistry):
    """Return a dataset with a separate column for each linker position.

    Requires Python lists in the linker_smiles column.
    Preserves their existing order and the original row index.
    """

    # Confirm that linker_smiles contains lists
    if not df_chemistry["linker_smiles"].apply(
        lambda value: isinstance(value, list)
    ).all():
        raise TypeError(
            "linker_smiles must contain Python lists. "
            "Load the pickle file or convert CSV strings to lists first."
        )

    # Copy the dataset before updating columns
    df_chemistry = df_chemistry.copy()

    # Identify previously created linker-position columns
    existing_linker_columns = [
        column for column in df_chemistry.columns
        if column.startswith("linker_")
        and column.removeprefix("linker_").isdigit()
    ]

    # Remove old positions so rerunning cannot leave stale linker columns
    df_chemistry = df_chemistry.drop(columns=existing_linker_columns)

    # Expand each linker list into a row of separate values
    linker_df = pd.DataFrame(
        df_chemistry["linker_smiles"].tolist(),
        index=df_chemistry.index
    )

    # Name the columns using the number of positions found
    linker_df.columns = [
        f"linker_{i}" for i in range(1, linker_df.shape[1] + 1)
    ]

    # Add all linker-position columns at once
    df_chemistry = pd.concat(
        [df_chemistry, linker_df],
        axis=1
    )

    return df_chemistry