import re,pathlib,subprocess,os,tempfile

link_pat = r"\[\[(.*)\]\]"

path = pathlib.Path.home() / "vimwiki"

index = path / "index.wiki"

def links_in_file(fpath):
    d = {fpath:[]}
    with open(fpath,"r",encoding="utf8") as f:
        fdata = [line.strip() for line in f.readlines()]
    links = list()
    for line in fdata:
        for link in re.findall(link_pat,line):
            linked = (path/link).with_suffix(".wiki")
            if linked.exists():
                links.append(links_in_file(linked))
    d[fpath] = links
    return d

links = links_in_file(index)


graphls = list()

def graph(d,ls):
    for k,v in d.items():
        for vv in v:
            for vvk,vvv in vv.items():
                vn = vvk.name
                ls.append(f"\"{k.name}\" -> \"{vn}\";")
            graph(vv,ls)

graph(links,graphls)

fmt = """
digraph foograph {
fontname="Helvetica,Arial,sans-serif";
node[fontname="Helvetica,Arial,sans-serif" color = "#00ff22" fontcolor="#f8f8f8"];
edge[fontname="Helvetica,Arial,sans-serif" color = "cyan" fontcolor="#f8f8f8"];
layout=twopi;
graph[ranksep=3,overlap=voronoi bgcolor="#1e1e2e"];
%s
}
"""
tfname = None
with tempfile.NamedTemporaryFile(mode="w",encoding="utf8",suffix=".dot",delete=False) as f:
    f.write(fmt % "\n".join(graphls))
    tfname = f.name
if tfname:
    pfname = None
    with tempfile.NamedTemporaryFile(suffix=".png",delete=False) as pf:
        pfname = pf.name
    if pfname:
        subprocess.run(["dot","-Tpng","-o"+pfname,tfname])
        os.startfile(pfname)
