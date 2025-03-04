from ase.build import graphene
from ase.io import write

# Define the graphene structure
# Ensure the size parameter is correctly defined as a tuple of three integers (x, y, z).
# Here, (1, 1, 1) creates the smallest unit cell with a single layer. Adjust this as needed.
structure = graphene(a=2.46, size=(1, 1, 1), vacuum=10.0)

# Save the structure to a CIF file
write("graphene.cif", structure)

print("Graphene CIF file has been generated and saved as 'graphene.cif'")
