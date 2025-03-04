from ase.build import graphene, make_supercell
from ase.io import write
import numpy as np

# Define the lattice constant for AlP (in angstroms)
a = 3.82  # Example value, adjust based on desired lattice constant

# Create a 2D honeycomb-like AlP structure based on graphene
alp_structure = graphene(a=a, size=(1, 1, 1), vacuum=10.0)

# Replace atomic species to represent AlP
symbols = ["Al", "P"] * (len(alp_structure) // 2)
alp_structure.set_chemical_symbols(symbols)

# Optionally transform into a rectangular cell
transformation_matrix = np.array([[1, 1, 0], [1, -1, 0], [0, 0, 1]])
alp_rectangular_structure = make_supercell(alp_structure, transformation_matrix)

# Save the AlP 2D structure to a CIF file
write("alp_2d.cif", alp_rectangular_structure)

print("AlP 2D nanostructure CIF file has been generated and saved as 'alp_2d.cif'")
