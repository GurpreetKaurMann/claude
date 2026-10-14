# -*- coding: utf-8 -*-
# pyRevit (IronPython) script, Revit 2024.
# Creates worksets for Conduit and Conduit Fitting per voltage class (HV / MV / LV), moves the
# matching elements into them, makes one view filter per voltage class (+ a panels filter) and
# applies soft colors in the ACTIVE view. Model must be workshared and saved.
# Edit CONFIG for how voltage class is marked in YOUR model.
from System.Collections.Generic import List
from pyrevit import revit, DB, forms

doc = revit.doc
view = revit.active_view

CONFIG = {
    # Instance parameter holding the voltage class text (Comments by default).
    "param": DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS,
    "classes": [  # soft colors
        {"key": "HV", "rgb": (240, 150, 150)},   # soft red
        {"key": "MV", "rgb": (245, 200, 120)},   # soft amber
        {"key": "LV", "rgb": (140, 185, 230)},   # soft blue
    ],
    "cats": [
        ("Conduit", DB.BuiltInCategory.OST_Conduit),
        ("Conduit Fitting", DB.BuiltInCategory.OST_ConduitFitting),
    ],
    "panels": {"filter": "ELEC EQUIPMENT - PANELS", "rgb": (245, 190, 130)},
    "surface_transparency": 30,
}

if not doc.IsWorkshared:
    forms.alert("Model is not workshared. Enable Worksharing (Collaborate tab) and save first.",
                exitscript=True)

def get_or_make_workset(name):
    for ws in DB.FilteredWorksetCollector(doc).OfKind(DB.WorksetKind.UserWorkset):
        if ws.Name == name:
            return ws
    return DB.Workset.Create(doc, name)

def get_filter(name):
    for f in DB.FilteredElementCollector(doc).OfClass(DB.ParameterFilterElement):
        if f.Name == name:
            return f

def contains_rule(pid, text):
    try:
        return DB.ParameterFilterRuleFactory.CreateContainsRule(pid, text)          # 2022+
    except TypeError:
        return DB.ParameterFilterRuleFactory.CreateContainsRule(pid, text, False)   # <=2021

solid = [p for p in DB.FilteredElementCollector(doc).OfClass(DB.FillPatternElement)
         if p.GetFillPattern().IsSolidFill]

def soft_override(rgb):
    col = DB.Color(*rgb)
    ogs = DB.OverrideGraphicSettings()
    ogs.SetProjectionLineColor(col)
    ogs.SetCutLineColor(col)
    if solid:
        ogs.SetSurfaceForegroundPatternId(solid[0].Id)
        ogs.SetSurfaceForegroundPatternColor(col)
    ogs.SetSurfaceTransparency(CONFIG["surface_transparency"])
    return ogs

def apply_to_view(pf, rgb):
    if not view.GetFilters().Contains(pf.Id):
        view.AddFilter(pf.Id)
    view.SetFilterOverrides(pf.Id, soft_override(rgb))
    view.SetFilterVisibility(pf.Id, True)

pid = DB.ElementId(CONFIG["param"])
all_cat_ids = List[DB.ElementId]([DB.ElementId(c) for _, c in CONFIG["cats"]])

with revit.Transaction("Conduit worksets + soft color filters"):
    for cls in CONFIG["classes"]:
        key = cls["key"]
        # worksets + move elements, one workset per category per class
        for label, cat in CONFIG["cats"]:
            ws = get_or_make_workset("{} {}".format(key, label))
            moved = 0
            for el in DB.FilteredElementCollector(doc).OfCategory(cat).WhereElementIsNotElementType():
                p = el.get_Parameter(CONFIG["param"])
                if p and p.AsString() and key in p.AsString():
                    wp = el.get_Parameter(DB.BuiltInParameter.ELEM_PARTITION_PARAM)
                    if wp and not wp.IsReadOnly:
                        wp.Set(ws.Id.IntegerValue)
                        moved += 1
            print("{} {}: moved {} elements".format(key, label, moved))

        # one filter per class covering conduit + fittings
        fname = "CONDUIT - {}".format(key)
        elf = DB.ElementParameterFilter(contains_rule(pid, key))
        pf = get_filter(fname)
        if pf is None:
            pf = DB.ParameterFilterElement.Create(doc, fname, all_cat_ids, elf)
        else:
            pf.SetElementFilter(elf)
        apply_to_view(pf, cls["rgb"])
        print("Filter '{}' applied".format(fname))

    # electrical equipment / panels
    cfg = CONFIG["panels"]
    pf = get_filter(cfg["filter"])
    if pf is None:
        pf = DB.ParameterFilterElement.Create(
            doc, cfg["filter"], List[DB.ElementId]([DB.ElementId(DB.BuiltInCategory.OST_ElectricalEquipment)]))
    apply_to_view(pf, cfg["rgb"])
    print("Filter '{}' applied".format(cfg["filter"]))
