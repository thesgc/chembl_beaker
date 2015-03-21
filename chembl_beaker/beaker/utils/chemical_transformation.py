__author__ = 'mnowotka'

#-----------------------------------------------------------------------------------------------------------------------

from rdkit.Chem.AllChem import Compute2DCoords

#-----------------------------------------------------------------------------------------------------------------------

def _computeCoords(mol, force=False):
    if force or (not mol.GetNumConformers() or mol.GetConformer().Is3D()):
        Compute2DCoords(mol)
    return mol

#-----------------------------------------------------------------------------------------------------------------------
