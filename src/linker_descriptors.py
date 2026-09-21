# Import pandas to check whether a SMILES value is missing
import pandas as pd

# Import Chem to convert a SMILES string into an RDKit molecule
from rdkit import Chem

# Import Descriptors to calculate numerical properties of each linker
from rdkit.Chem import Descriptors

# Calculate the 15 selected descriptors for one linker
def calculate_all_descriptors(smiles):
    """Return a dictionary of descriptors for one linker SMILES.

    Missing or unparseable SMILES return NaN for all 15 descriptors.
    """

    # Define missing values using the same names as the calculated descriptors
    missing_descriptors = {
        "MolWt": float("nan"),
        "TPSA": float("nan"),
        "NumHAcceptors": float("nan"),
        "NumHDonors": float("nan"),
        "NumAromaticRings": float("nan"),
        "MaxPartialCharge": float("nan"),
        "MinPartialCharge": float("nan"),
        "NOCount": float("nan"),
        "NumHeteroatoms": float("nan"),
        "LogP": float("nan"),
        "LabuteASA": float("nan"),
        "RotatableBonds": float("nan"),
        "FractionCSP3": float("nan"),
        "PEOE_VSA1": float("nan"),
        "PEOE_VSA2": float("nan"),
    }

    # Return missing descriptors for None, NaN, or an empty SMILES string
    if pd.isna(smiles) or smiles.strip() == "":
        return missing_descriptors

    # Convert the SMILES string into an RDKit molecule
    mol = Chem.MolFromSmiles(smiles)

    # Report unparseable SMILES and return missing descriptors
    if mol is None:
        print("RDKit could not read this SMILES:", smiles)
        return missing_descriptors

    # Calculate and return the selected linker descriptors
    return {
        # Molecular weight
        "MolWt": Descriptors.MolWt(mol),

        # Topological polar surface area
        "TPSA": Descriptors.TPSA(mol),

        # Hydrogen-bond acceptor and donor counts
        "NumHAcceptors": Descriptors.NumHAcceptors(mol),
        "NumHDonors": Descriptors.NumHDonors(mol),

        # Number of aromatic rings
        "NumAromaticRings": Descriptors.NumAromaticRings(mol),

        # Maximum and minimum estimated atomic partial charges
        "MaxPartialCharge": Descriptors.MaxPartialCharge(mol),
        "MinPartialCharge": Descriptors.MinPartialCharge(mol),

        # Combined nitrogen and oxygen count
        "NOCount": Descriptors.NOCount(mol),

        # Number of atoms other than carbon and hydrogen
        "NumHeteroatoms": Descriptors.NumHeteroatoms(mol),

        # Estimated octanol/water partition coefficient
        "LogP": Descriptors.MolLogP(mol),

        # Approximate linker molecular surface area
        "LabuteASA": Descriptors.LabuteASA(mol),

        # Number of rotatable bonds
        "RotatableBonds": Descriptors.NumRotatableBonds(mol),

        # Fraction of carbon atoms with sp3 hybridization
        "FractionCSP3": Descriptors.FractionCSP3(mol),

        # Surface contributions from atoms with partial charge below -0.30
        "PEOE_VSA1": Descriptors.PEOE_VSA1(mol),

        # Surface contributions from atoms with -0.30 <= charge < -0.25
        "PEOE_VSA2": Descriptors.PEOE_VSA2(mol),
    }