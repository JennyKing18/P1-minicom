#!/usr/bin/env python3
import json, urllib.request, urllib.parse, collections

PROJ  = "JennyKing18_P1-minicom"
ORG   = "jennyking18"
FILES = ["config.c", "dial.c", "updown.c"]
KEYS  = ",".join(f"{PROJ}:minicom-2.10/src/{f}" for f in FILES)

def api(path, **p):
    url = f"https://sonarcloud.io/api/{path}?" + urllib.parse.urlencode(p)
    return json.load(urllib.request.urlopen(url, timeout=60))

issues, page = [], 1
while True:
    d = api("issues/search", componentKeys=KEYS, types="VULNERABILITY,BUG",
            resolved="false", ps=500, p=page)
    issues += d["issues"]
    if len(issues) >= d["total"]:
        break
    page += 1

cwe = {}
for r in {i["rule"] for i in issues}:
    j = api("rules/show", organization=ORG, key=r)["rule"]
    cwe[r] = ", ".join("CWE-" + s.split(":")[1]
                       for s in j.get("securityStandards", [])
                       if s.startswith("cwe")) or "-"

with open("sonar-tabla.csv", "w", encoding="utf-8") as fh:
    fh.write("archivo,linea,cwe,regla,tipo,severidad,mensaje\n")
    for i in sorted(issues, key=lambda x: (x["component"], x.get("line", 0))):
        f   = i["component"].split("/")[-1]
        msg = i["message"].replace('"', "'")
        fh.write(f'{f},{i.get("line","")},"{cwe[i["rule"]]}",{i["rule"]},'
                 f'{i["type"]},{i.get("severity","")},"{msg}"\n')

print(f"{len(issues)} issues -> sonar-tabla.csv\n")
for f, n in collections.Counter(i["component"].split("/")[-1]
                                for i in issues).most_common():
    print(f"  {n:3}  {f}")
