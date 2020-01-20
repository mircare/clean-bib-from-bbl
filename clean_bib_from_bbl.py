import os, sys

if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"file.bbl file.bib")
    exit()

good = []
with open(sys.argv[1], "r") as bbl:
    for line in bbl:
        if "\\bibitem{" in line:
            good.append(line.replace("\\bibitem{","").replace("}","").strip())
        elif "}]{" in line:
            good.append(line.split("}]{")[1].replace("}\n",""))
        elif "]{" in line:
            good.append(line.split("]{")[1].replace("}\n",""))

bib = open(sys.argv[2], "r")
with open("clean.bib", "w") as out:
    found = False
    abstract = False
    for line in bib:
        if found:
            if "}\n" == line:
                found = False
                out.write(line+"\n")
            elif "	abstract = {" in line:
                abstract = True
            elif abstract and "\t" in line and " = {" in line:
                abstract = False
                out.write(line)
            elif not abstract and "keywords" not in line and "urldate" not in line:
                out.write(line)
        elif "@" in line[0]:
            if line.strip().split("{")[1].replace(",","") in good:
                found = True
                out.write(line)
