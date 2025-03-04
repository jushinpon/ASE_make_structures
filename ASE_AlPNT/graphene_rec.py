from ase.build import graphene, make_supercell
from ase.io import write
import numpy as np

# Define the graphene structure
structure = graphene(a=2.46, size=(1, 1, 1), vacuum=10.0)

# Define the transformation matrix to convert the hexagonal cell into a rectangular cell
# This matrix reshapes the unit cell while preserving the graphene structure
transformation_matrix = np.array([[1, 1, 0], [1, -1, 0], [0, 0, 1]])

# Apply the transformation to create a rectangular cell
rectangular_structure = make_supercell(structure, transformation_matrix)

# Save the rectangular cell structure to a CIF file
write("rectangular_graphene.cif", rectangular_structure)

print("Rectangular graphene CIF file has been generated and saved as 'rectangular_graphene.cif'")
