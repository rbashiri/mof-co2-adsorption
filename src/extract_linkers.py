# Import RDKit tools for reading SMILES and processing molecular fragments
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
    "[Zn][Zn]",  # Zinc dimer
    "[Cu][Cu]",  # Copper dimer
    "[O]",       # Isolated neutral oxygen atom
    "[Zn+3][Zn+5]",  # Charged zinc fragment found during validation
    
}
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

        # Remove exact unwanted standalone fragments
        fragment_smiles = Chem.MolToSmiles(frag)

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

            linker_smiles.append(fragment_smiles)

        except Exception as error:
            # Record the rejected fragment and its error message
            invalid_fragments.append({
                "fragment": Chem.MolToSmiles(frag),
                "error": str(error)
            })

    return linker_smiles, invalid_fragments