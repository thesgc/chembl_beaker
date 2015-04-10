__author__ = 'mnowotka'

#-----------------------------------------------------------------------------------------------------------------------

import StringIO
from rdkit.Chem import Draw, SanitizeMol
from rdkit import Chem
from chembl_beaker.beaker.utils.functional import _apply
from chembl_beaker.beaker.utils.chemical_transformation import _computeCoords
from chembl_beaker.beaker.utils.io import _parseMolData, _parseSMILESData

#-----------------------------------------------------------------------------------------------------------------------

def _mols2imageStream(mols, f, format, size, legend):
    image = Draw.MolsToGridImage(mols,molsPerRow=min(len(mols),4),subImgSize=(size,size),
                                    legends=[x.GetProp("_Name") if x.HasProp("_Name") else legend for x in mols])
    image.save(f, format)

#-----------------------------------------------------------------------------------------------------------------------

def _mols2imageString(mols,size,legend, format, recalc=True):
    if not mols:
        return ''
    if recalc:
        _apply(mols, _computeCoords)
    imageData = StringIO.StringIO()
  #  for mol in mols:
        #SanitizeMol(mol,sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL^Chem.SanitizeFlags.SANITIZE_CLEANUPCHIRALITY)
 #       Chem.AssignAtomChiralTagsFromStructure(mol,replaceExistingTags=False)
    _mols2imageStream(mols, imageData, format, size, legend)
    return imageData.getvalue()

#-----------------------------------------------------------------------------------------------------------------------

def _ctab2image(data,size,legend, recalc=True):
    return _mols2imageString(_parseMolData(data),size,legend, 'PNG', recalc=recalc)

#-----------------------------------------------------------------------------------------------------------------------

def _smiles2image(data,size,legend):
    return _mols2imageString(_parseSMILESData(data), size, legend, 'PNG', recalc=recalc)

#-----------------------------------------------------------------------------------------------------------------------
