import os
import shutil
import numpy as np
from ase.build import nanotube
from ase.io import write

# Define the folder to store CIF files
output_folder = "AlPNT"

# Remove the old folder and create a new one
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)  # Remove existing folder and its contents
os.makedirs(output_folder)  # Create a new folder

def calculate_nanotube_diameter(n, m, bond_length):
    """
    Calculate the nanotube diameter based on chiral indices and bond length.

    Parameters:
    - n, m: Chiral indices (integer)
    - bond_length: Float, bond length in Å.

    Returns:
    - Float, nanotube diameter in Å.
    """
    a = bond_length * np.sqrt(3)  # Lattice constant
    d = (a / np.pi) * np.sqrt(n**2 + n*m + m**2)  # Nanotube diameter formula
    return d

def create_alp_nanotube(chiral_indices, bond_length, chiral_type, filename, vacuum_buffer=5):
    """
    Create an AlP nanotube based on a CNT structure and save it as a CIF file in the AlPNT folder.

    Parameters:
    - chiral_indices: Tuple of two integers (n, m).
    - bond_length: Float, bond length in Å.
    - chiral_type: String, type of nanotube (e.g., 'zigzag', 'armchair', 'chiral').
    - filename: String, output CIF filename (without folder path).
    - vacuum_buffer: Float, additional vacuum space added to the nanotube diameter.
    """
    n, m = chiral_indices
    diameter = calculate_nanotube_diameter(n, m, bond_length)
    vacuum = diameter + vacuum_buffer  # Vacuum spacing = NT diameter + buffer

    # Generate a carbon nanotube structure
    cnt = nanotube(n=n, m=m, bond=bond_length)

    # Replace carbon atoms with alternating Al and P
    symbols = ['Al' if j % 2 == 0 else 'P' for j in range(len(cnt))]
    cnt.set_chemical_symbols(symbols)

    # Set vacuum in the x and y directions
    cnt.cell = [vacuum, vacuum, cnt.cell[2, 2]]  # Keep original length in z
    cnt.center()  # Center the nanotube in the unit cell
    cnt.pbc = [True, True, True]  # Periodic boundary conditions

    # Embed chiral info
    cnt.info['Chiral indices'] = f"({n}, {m})"

    # Full path for CIF file
    file_path = os.path.join(output_folder, filename)

    # Save the structure as a CIF file
    write(file_path, cnt, format='cif')
    print(f"AlP nanotube ({chiral_type}) with chiral indices {cnt.info['Chiral indices']} saved as {file_path}, vacuum = {vacuum:.2f} Å")

# Global parameters: number of nanotubes to generate for each type
num_armchair = 5  # Number of armchair nanotubes
num_zigzag = 5    # Number of zigzag nanotubes
num_chiral = 4    # Number of chiral nanotubes

# Radius increment control
radius_increment_armchair = 3  # Increase in (n, n) index
radius_increment_zigzag = 3    # Increase in (n, 0) index
radius_increment_chiral = 1    # Increase in (n, m) index

# Bond lengths for each type
bond_lengths = {
    "armchair": 2.25,
    "zigzag": 2.27,
    "chiral": 2.27
}

# Custom vacuum buffer (Change this value as needed)
custom_vacuum_buffer = 6  # This is the extra vacuum space added to the NT diameter

# Generate armchair AlP NTs
start_n = 3
for i in range(num_armchair):
    n = start_n + i * radius_increment_armchair
    create_alp_nanotube(
        chiral_indices=(n, n),
        bond_length=bond_lengths["armchair"],
        chiral_type="armchair",
        filename=f"A_AlPNT_{n}x{n}.cif",
        vacuum_buffer=custom_vacuum_buffer
    )

# Generate zigzag AlP NTs
start_n = 3
for i in range(num_zigzag):
    n = start_n + i * radius_increment_zigzag
    create_alp_nanotube(
        chiral_indices=(n, 0),
        bond_length=bond_lengths["zigzag"],
        chiral_type="zigzag",
        filename=f"Z_AlPNT_{n}x0.cif",
        vacuum_buffer=custom_vacuum_buffer
    )

# Generate chiral AlP NTs
start_n = 3
for i in range(num_chiral):
    n = start_n + i * radius_increment_chiral
    m = max(n - 2, 1)  # Ensuring valid chiral indices
    create_alp_nanotube(
        chiral_indices=(n, m),
        bond_length=bond_lengths["chiral"],
        chiral_type="chiral",
        filename=f"C_AlPNT_{n}x{m}.cif",
        vacuum_buffer=custom_vacuum_buffer
    )
