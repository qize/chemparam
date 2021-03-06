# Methods for parsing a PSF file.
from numpy import array, reshape

#import sys, os # required for relative import
#dn = os.path.dirname
#sys.path.append(dn(dn(os.path.abspath(__file__))))
from mol import Mol

__all__ = ["read_psf"]

# PSF header - skip 2 lines, then read a title
# File -> IO(String)
def read_title(f):
    f.readline() # skip 2
    f.readline()
    n = int(f.readline().split()[0])
    title = ""
    for i in range(n):
        title += f.readline()
    return title

# ck_section(f, "!NATOM") will
# read until parsing a line like, "14 !NATOM",
# and return 14 (or else throw an exception)
# File, String -> IO(Int)
def ck_section(f, name):
    while(True):
        line = f.readline()
        tok = line.split()
        if len(tok) < 2:
            continue
        if tok[1] == name:
            return int(tok[0])
        else:
            raise ValueError, "Expected section %s, found: %s"%(name, line)

# File -> IO([Atom])
def read_atoms(f):
    n = ck_section(f, "!NATOM")
    a = []
    for i in range(n):
        a.append(Atom(f.readline()))
    return a

# File -> IO(Array Int)
def read_bonds(f):
    n = ck_section(f, "!NBOND:")
    # Reshaping will verify the number of bonds actually read.
    return reshape(array(read_ints(f))-1, (n,2))

# Read ints until encountering a blank line
# File -> IO(Array Int)
def read_ints(f):
    l = []
    while(True):
        tok = f.readline().split()
        if len(tok) < 1:
            return l
        l += map(int, tok)

# String -> IO(Mol)
def read_psf(name):
    with open(name, 'r') as f:
        title = read_title(f)
        atoms = read_atoms(f)
        bonds = read_bonds(f)
    return Mol(atoms, bonds)

# parse an atom line into a dict
# e.g.
#"14 BUTA     1        BUTA     C4        320  -0.270000       12.0110 0   0.00000     -0.301140E-02"
def Atom(line):
    tok = line.split()
    return { 'n': int(tok[0]),
             'chain': tok[1],
             'resn': int(tok[2]),
             'res': tok[3],
             'name': tok[4],
             't': tok[5],
             'q': float(tok[6]),
             'm': float(tok[7]),
             'x': [0.0, 0.0, 0.0]}

def test():
     f = read_psf("../../data/glucose.psf")
     f.write_psf("tmp.psf")

