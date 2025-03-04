from ase.build import nanotube
from ase.io import write

def create_alp_nanotube(chiral_indices, bond_length, chiral_type, filename):
    """
    Create an AlP nanotube based on a CNT structure and save it as a CIF file.

    Parameters:
    - chiral_indices: Tuple of two integers, e.g., (5, 0) for zigzag, (3, 3) for armchair, or (5, 3) for chiral.
    - bond_length: Float, bond length in Å.
    - chiral_type: String, type of nanotube (e.g., 'zigzag', 'armchair', or 'chiral').
    - filename: String, output CIF filename.
    """
    # Generate a carbon nanotube structure
    cnt = nanotube(n=chiral_indices[0], m=chiral_indices[1], bond=bond_length)

    # Replace carbon atoms with alternating Al and P
    symbols = ['Al' if i % 2 == 0 else 'P' for i in range(len(cnt))]
    cnt.set_chemical_symbols(symbols)

    # Add vacuum in the x and y directions for isolation
    vacuum = 20.0  # 20 Å vacuum spacing
    cnt.cell = [vacuum, vacuum, cnt.cell[2, 2]]  # Keep original length in z, add vacuum in x and y
    cnt.center()  # Center the nanotube in the unit cell
    cnt.pbc = [True, True, True]  # Periodic boundary conditions

    # Save the structure as a CIF file
    write(filename, cnt, format='cif')  # Directly pass the filename
    print(f"AlP nanotube ({chiral_type}) saved as {filename}")

# Parameters for the three types of AlP nanotubes
nanotubes_params = [
    {
        "chiral_indices": (5, 0),  # Zigzag
        "bond_length": 2.27,
        "chiral_type": "zigzag",
        "filename": "Z_AlPNT.cif"
    },
    {
        "chiral_indices": (3, 3),  # Armchair
        "bond_length": 2.25,
        "chiral_type": "armchair",
        "filename": "A_AlPNT.cif"
    },
    {
        "chiral_indices": (5, 3),  # Chiral
        "bond_length": 2.27,
        "chiral_type": "chiral",
        "filename": "C_AlPNT.cif"
    }
]

# Generate and save all three AlP nanotubes
for params in nanotubes_params:
    create_alp_nanotube(**params)
