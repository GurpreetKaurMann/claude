# -*- coding: utf-8 -*-
# pyRevit script, Revit 2024: creates only the "HV Conduit" and "LV Conduit" user worksets.
from pyrevit import revit, DB, forms

doc = revit.doc
if not doc.IsWorkshared:
    forms.alert("Model is not workshared. Enable Worksharing (Collaborate tab) and save first.", exitscript=True)

existing = [w.Name for w in DB.FilteredWorksetCollector(doc).OfKind(DB.WorksetKind.UserWorkset)]
for name in ("HV Conduit", "LV Conduit"):
    if name in existing:
        print("Exists: " + name)
    else:
        DB.Workset.Create(doc, name)   # Workset.Create manages its own change; no Transaction needed
        print("Created: " + name)
