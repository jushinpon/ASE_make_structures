import os
import shutil
from ase.build import nanotube
from ase.io import write

# Define the folder to store CIF files
output_folder = "AlPNT"

# Remove the old folder and create a new one
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)  # Remove existing folder and its contents
os.makedirs(output_folder)  # Create a new folder

def create_alp_nanotube(chiral_indices, bond_length, chiral_type, filename):
    """
    Create an AlP nanotube based on a CNT structure and save it as a CIF file in the AlPNT folder.

    Parameters:
    - chiral_indices: Tuple of two integers (n, m).
    - bond_length: Float, bond length in Å.
    - chiral_type: String, type of nanotube (e.g., 'zigzag', 'armchair', 'chiral').
    - filename: String, output CIF filename (without folder path).
    """
    # Generate a carbon nanotube structure
    cnt = nanotube(n=chiral_indices[0], m=chiral_indices[1], bond=bond_length)

    # Replace carbon atoms with alternating Al and P
    symbols = ['Al' if j % 2 == 0 else 'P' for j in range(len(cnt))]
    cnt.set_chemical_symbols(symbols)

    # Add vacuum in the x and y directions for isolation
    vacuum = 20.0  # 20 Å vacuum spacing
    cnt.cell = [vacuum, vacuum, cnt.cell[2, 2]]  # Keep original length in z, add vacuum in x and y
    cnt.center()  # Center the nanotube in the unit cell
    cnt.pbc = [True, True, True]  # Periodic boundary conditions

    # Embed chiral info
    cnt.info['Chiral indices'] = f"({chiral_indices[0]}, {chiral_indices[1]})"

    # Full path for CIF file
    file_path = os.path.join(output_folder, filename)

    # Save the structure as a CIF file
    write(file_path, cnt, format='cif')
    print(f"AlP nanotube ({chiral_type}) with chiral indices {cnt.info['Chiral indices']} saved as {file_path}")

# Global parameters: number of nanotubes to generate for each type
num_armchair = 5  # Number of armchair nanotubes
num_zigzag = 5    # Number of zigzag nanotubes
num_chiral = 5    # Number of chiral nanotubes

# Radius increment control
radius_increment_armchair = 3  # Increase in (n, n) index
radius_increment_zigzag = 3    # Increase in (n, 0) index
radius_increment_chiral = 2    # Increase in (n, m) index

# Bond lengths for each type
bond_lengths = {
    "armchair": 2.25,
    "zigzag": 2.27,
    "chiral": 2.27
}

# Generate armchair AlP NTs
start_n = 3
for i in range(num_armchair):
    n = start_n + i * radius_increment_armchair
    create_alp_nanotube(
        chiral_indices=(n, n),
        bond_length=bond_lengths["armchair"],
        chiral_type="armchair",
        filename=f"A_AlPNT_{n}x{n}.cif"
    )

# Generate zigzag AlP NTs
start_n = 3
for i in range(num_zigzag):
    n = start_n + i * radius_increment_zigzag
    create_alp_nanotube(
        chiral_indices=(n, 0),
        bond_length=bond_lengths["zigzag"],
        chiral_type="zigzag",
        filename=f"Z_AlPNT_{n}x0.cif"
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
        filename=f"C_AlPNT_{n}x{m}.cif"
    )
