import numpy as np

path_raw_file = "input/2024-04-02.csv"

# map centre here
# note: update if there are new centers
center_map = {
    "HEAD OFFICE": "HO",
    "SEDAYU CITY": "SDC",
    "KOTA KASABLANKA": "KK",
    "PACIFIC PLACE": "PP",
    "INDONESIA": "ID",
    "GANDARIA CITY": "GC",
    "LIVING WORLD": "LW",
    "DAGO": "DG",
    "PAKUWON": "PKW",
    "CENTRAL PARK": "CP",
    "BEKASI": "SMB",
    "BSD CITY": "BSD",
    "CIBUBUR": "CBB",
    "CIKARANG": "CKR",
    "SIMATUPANG": "TBS",
    "INDIES": "INDIES",
    "NATIONAL SALES TEAM": "NST",
    "REGIONAL SALES TEAM": "RST",
    "GO CENTER": "Online Center",
}

jkt_1 = ["PP", "SDC", "KG", "CKR"]
jkt_2 = ["GC", "LW", "BSD", "TBS", "CP"]
jkt_3 = ["KK", "CBB", "SMB"]
bdg = ["DG"]
sby = ["PKW"]
centers = jkt_1 + jkt_2 + jkt_3 + bdg + sby

map_areas = {
    "JKT 1": jkt_1,
    "JKT 2": jkt_2,
    "JKT 3": jkt_3,
    "BDG": bdg,
    "SBY": sby,
    "Other": ["HO", "Street Talk", "ID", "NST", "INDIES", "RST"],
    "Corporate": ["Corporate"],
    "Online Center": ["Online Center"],
}