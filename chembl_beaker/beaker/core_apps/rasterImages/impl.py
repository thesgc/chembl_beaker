__author__ = 'mnowotka'

#-----------------------------------------------------------------------------------------------------------------------

import StringIO
from rdkit.Chem import Draw, SanitizeMol
from rdkit import Chem
from chembl_beaker.beaker.utils.functional import _apply
from chembl_beaker.beaker.utils.chemical_transformation import _computeCoords
from chembl_beaker.beaker.utils.io import _parseMolData, _parseSMILESData
from rdkit.Chem import  SDMolSupplier, AllChem, Draw, SanitizeMol, SanitizeFlags,   AssignAtomChiralTagsFromStructure

#-----------------------------------------------------------------------------------------------------------------------

def _mols2imageStream(mols, f, format, size, legend, highlightMatch=None):
    highlights = None
    if highlightMatch:
        pattern = Chem.MolFromSmarts(highlightMatch)
        highlights = [mol.GetSubstructMatch(pattern) for mol in mols]
    kek = True
    if mols[0].HasProp("_drawingBondsWedged"):
        kek=False
    image = Draw.MolsToGridImage(mols,molsPerRow=min(len(mols),4),subImgSize=(size,size),
                                    legends=[ legend for x in mols], kekulize=kek,highlightAtomLists=highlights
 )
    image.save(f, format)

#-----------------------------------------------------------------------------------------------------------------------

def _mols2imageString(mols,size,legend, format, recalc=False, highlightMatch=None):
    if not mols:
        return ''
 #   if recalc:
  #      _apply(mols, _computeCoords)
    imageData = StringIO.StringIO()
    for mol in mols:
        try:
            SanitizeMol(mol,sanitizeOps=SanitizeFlags.SANITIZE_ALL^SanitizeFlags.SANITIZE_CLEANUPCHIRALITY^Chem.SanitizeFlags.SANITIZE_SETCONJUGATION^Chem.SanitizeFlags.SANITIZE_SETAROMATICITY)
        except ValueError:
            return imageData.getvalue()
        AllChem.AssignAtomChiralTagsFromStructure(mol,replaceExistingTags=False)
    _mols2imageStream(mols, imageData, format, size, legend, highlightMatch=highlightMatch)
    return imageData.getvalue()

#-----------------------------------------------------------------------------------------------------------------------

def _ctab2image(data,size,legend, recalc=True, highlightMatch=None):
    return _mols2imageString(_parseMolData(data),size,legend, 'PNG', recalc=recalc, highlightMatch=highlightMatch)

#-----------------------------------------------------------------------------------------------------------------------

def _smiles2image(data,size,legend):
    return _mols2imageString(_parseSMILESData(data), size, legend, 'PNG', recalc=recalc)

#-----------------------------------------------------------------------------------------------------------------------
