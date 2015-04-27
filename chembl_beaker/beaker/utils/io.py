__author__ = 'mnowotka'

#-----------------------------------------------------------------------------------------------------------------------

import StringIO
from rdkit.Chem import SDMolSupplier
from rdkit.Chem import SmilesMolSupplier
from rdkit.Chem import MolFromSmiles, MolToMolBlock
from rdkit.Chem import SDWriter
from rdkit.Chem import SmilesWriter
from chembl_beaker.beaker.utils.functional import _apply
from chembl_beaker.beaker.utils.chemical_transformation import _computeCoords
from rdkit.Chem import SanitizeMol
from rdkit.Chem.AllChem import Compute2DCoords

#-----------------------------------------------------------------------------------------------------------------------

def _parseMolData(data):
    suppl = SDMolSupplier()

    suppl.SetData(str(data), sanitize=False)
    data = [x for x in suppl if x]
    for x in data:
        if not x.HasProp("_drawingBondsWedged"):
            SanitizeMol(x)
        ctab = MolToMolBlock(x)
        ctablines = [item.split("0.0000") for item in ctab.split("\n") if "0.0000" in item]
        needs_redraw = 0
        for line in ctablines:
            if len(line) > 3:
                needs_redraw +=1
        if needs_redraw == len(ctablines):
             #check for overlapping molecules in the CTAB 
            Compute2DCoords(x)
            print "testr"
    return data


#-----------------------------------------------------------------------------------------------------------------------

def _parseSMILESData(data, computeCoords=False):
    suppl = SmilesMolSupplier()
    suppl.SetData(data)
    mols = [x for x in suppl if x]
    if not mols:
        mols = [MolFromSmiles(data)]
    if computeCoords:
        _apply(mols, _computeCoords, True)
    return mols

#-----------------------------------------------------------------------------------------------------------------------

def _getSDFStream(f, mols):
    w = SDWriter(f)
    for m in mols:
        w.write(m)
    w.flush()

#-----------------------------------------------------------------------------------------------------------------------

def _getSDFString(mols):
    sio = StringIO.StringIO()
    _getSDFStream(sio, mols)
    return sio.getvalue()

#-----------------------------------------------------------------------------------------------------------------------

def _getSMILESStream(f, mols):
    w = SmilesWriter(f, isomericSmiles=True)
    for mol in mols:
        w.write(mol)
    w.flush()

#-----------------------------------------------------------------------------------------------------------------------

def _getSMILESString(mols):
    sio = StringIO.StringIO()
    _getSMILESStream(sio, mols)
    return sio.getvalue()

#-----------------------------------------------------------------------------------------------------------------------
