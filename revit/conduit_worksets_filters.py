# -*- coding: utf-8 -*-
# pyRevit (IronPython) script: HV / LV conduit worksets + view filters with color overrides.
# Run from a pyRevit button/script in the model, in the view you want filtered.
# Edit CONFIG for how HV vs LV conduit is identified in YOUR model.
from System.Collections.Generic import List
from pyrevit import revit, DB, forms

doc = revit.doc
view = revit.active_view

CONFIG = {
    # Instance parameter that tells HV from LV (Comments by default).
    "param": DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS,
    "HV": {"match": "HV", "workset": "HV Conduit", "filter": "CONDUIT - HV", "rgb": (255, 0, 0)},
    "LV": {"match": "LV", "workset": "LV Conduit", "filter": "CONDUIT - LV", "rgb": (0, 112, 192)},
    "cats": [DB.BuiltInCategory.OST_Conduit, DB.BuiltInCategory.OST_ConduitFitting],
    # Electrical equipment / panels: category-only filter (no parameter rule), own color.
    "PANELS": {"filter": "ELEC EQUIPMENT - PANELS", "rgb": (255, 140, 0),
               "cats": [DB.BuiltInCategory.OST_ElectricalEquipment]},
}

if not doc.IsWorkshared:
    forms.alert("Model is not workshared. Enable Worksharing (Collaborate tab) first.", exitscript=True)

def get_or_make_workset(name):
    for ws in DB.FilteredWorksetCollector(doc).OfKind(DB.WorksetKind.UserWorkset):
        if ws.Name == name:
            return ws
    return DB.Workset.Create(doc, name)

def get_filter(name):
    for f in DB.FilteredElementCollector(doc).OfClass(DB.ParameterFilterElement):
        if f.Name == name:
            return f
    return None

def contains_rule(pid, text):
    try:
        return DB.ParameterFilterRuleFactory.CreateContainsRule(pid, text)          # 2022+
    except TypeError:
        return DB.ParameterFilterRuleFactory.CreateContainsRule(pid, text, False)   # <=2021

cat_ids = [DB.ElementId(c) for c in CONFIG["cats"]]
pid = DB.ElementId(CONFIG["param"])
solid = [p for p in DB.FilteredElementCollector(doc).OfClass(DB.FillPatternElement)
         if p.GetFillPattern().IsSolidFill]

with revit.Transaction("HV/LV conduit worksets + filters"):
    for key in ("HV", "LV"):
        cfg = CONFIG[key]
        ws = get_or_make_workset(cfg["workset"])

        # --- move matching conduit + fittings to the workset
        moved = 0
        for cat in CONFIG["cats"]:
            for el in DB.FilteredElementCollector(doc).OfCategory(cat).WhereElementIsNotElementType():
                p = el.get_Parameter(CONFIG["param"])
                if p and p.AsString() and cfg["match"] in p.AsString():
                    wp = el.get_Parameter(DB.BuiltInParameter.ELEM_PARTITION_PARAM)
                    if wp and not wp.IsReadOnly:
                        wp.Set(ws.Id.IntegerValue); moved += 1

        # --- filter
        pf = get_filter(cfg["filter"])
        rule = contains_rule(pid, cfg["match"])
        elf = DB.ElementParameterFilter(rule)
        if pf is None:
            pf = DB.ParameterFilterElement.Create(doc, cfg["filter"], List[DB.ElementId](cat_ids), elf)
        else:
            pf.SetElementFilter(elf)

        # --- apply to view + color
        if not view.GetFilters().Contains(pf.Id):
            view.AddFilter(pf.Id)
        ogs = DB.OverrideGraphicSettings()
        col = DB.Color(*cfg["rgb"])
        ogs.SetProjectionLineColor(col)
        ogs.SetCutLineColor(col)
        if solid:
            ogs.SetSurfaceForegroundPatternId(solid[0].Id)
            ogs.SetSurfaceForegroundPatternColor(col)
        view.SetFilterOverrides(pf.Id, ogs)
        view.SetFilterVisibility(pf.Id, True)
        print("{}: moved {} elements to '{}', filter '{}' applied".format(key, moved, cfg["workset"], cfg["filter"]))

    # --- electrical equipment (panels) filter: all categories, no parameter rule
    cfg = CONFIG["PANELS"]
    pf = get_filter(cfg["filter"])
    if pf is None:
        pf = DB.ParameterFilterElement.Create(
            doc, cfg["filter"], List[DB.ElementId]([DB.ElementId(c) for c in cfg["cats"]]))
    if not view.GetFilters().Contains(pf.Id):
        view.AddFilter(pf.Id)
    ogs = DB.OverrideGraphicSettings()
    col = DB.Color(*cfg["rgb"])
    ogs.SetProjectionLineColor(col)
    ogs.SetCutLineColor(col)
    if solid:
        ogs.SetSurfaceForegroundPatternId(solid[0].Id)
        ogs.SetSurfaceForegroundPatternColor(col)
    view.SetFilterOverrides(pf.Id, ogs)
    view.SetFilterVisibility(pf.Id, True)
    print("Panels: filter '{}' applied".format(cfg["filter"]))
