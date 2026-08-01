# reuse the standard CO2 pressures reported in this dataset
CO2_PRESSURES = [0.01, 0.05, 0.1, 0.5, 2.5]

# import the built-in library for reading/parsing JSON files
import json

# import Path, a convenient way to build and work with file/folder paths
from pathlib import Path


# function to parse one JSON file into a flat dict of structural + CO2 features
def parse_one_mof(json_path):
    # open the JSON file for reading
    with open(json_path) as f:
        # load the JSON content into a Python dictionary
        data = json.load(f)

    # build the base row with structural properties pulled straight from the JSON
    row = {
        # use the filename (without extension) as a unique identifier
        "filename": Path(json_path).stem,
        # largest cavity diameter
        "lcd": data.get("lcd"),
        # pore limiting diameter
        "pld": data.get("pld"),
        # fraction of accessible void volume
        "void_fraction": data.get("void_fraction"),
        # gravimetric surface area (m^2/g)
        "surface_area_m2g": data.get("surface_area_m2g"),
        # SMILES string describing the linker, used later for RDKit features
        "mofid": data.get("mofid"),
    }

    # pre-create one CO2 uptake column per standard pressure, default to missing
    for p in CO2_PRESSURES:
        row[f"CO2_uptake_{p}bar_molkg"] = None

    # loop through every isotherm entry recorded for this MOF
    for entry in data.get("isotherms", []):
        # get the list of adsorbate gases for this isotherm entry
        adsorbates = entry.get("adsorbates", [])
        # skip this entry if there's no adsorbate listed, or it isn't CO2
        if not adsorbates or adsorbates[0].get("name") != "CarbonDioxide":
            continue
        # skip this entry if the units aren't mol/kg (we don't want kJ/mol heat data here)
        if entry.get("adsorptionUnits") != "mol/kg":
            continue
        # loop through each individual pressure/uptake data point in this isotherm
        for point in entry.get("isotherm_data", []):
            # pull out the pressure and the corresponding total adsorption value
            p, uptake = point.get("pressure"), point.get("total_adsorption")
            # check this pressure against each of our standard target pressures
            for target_p in CO2_PRESSURES:
                # if the pressure is close enough to a standard value, record the uptake
                if p is not None and abs(p - target_p) < 1e-3:
                    row[f"CO2_uptake_{target_p}bar_molkg"] = uptake
    # return the completed row for this one MOF
    return row


# allow this file to be run directly from the command line for a quick test
if __name__ == "__main__":
    # import sys to read command-line arguments
    import sys

    # loop through each file path passed as a command-line argument
    for fname in sys.argv[1:]:
        # parse the file and print the resulting row as formatted JSON
        result = parse_one_mof(fname)
        print(json.dumps(result, indent=2))