import yaml
import jinja2
import re
from datetime import date
from collections import defaultdict

def parse_yaml(paper_data):
    with open(paper_data) as fh:
        raw = yaml.safe_load(fh)

    papers = raw.keys()
    ans = {'papers': raw}

    peer_years =  defaultdict(list)
    other_years = defaultdict(list)
    firstlast = 0
    for k in papers:
        year = k[:4]
        cat = ans['papers'][k]["category"]
        if "book" in cat:
            other_years[year].append(k)
        elif "preprints" in cat:
            peer_years['submitted'].append(k)
            if "flc" in cat or 'math' in cat:
                firstlast += 1
        else:
            peer_years[year].append(k)
            if "flc" in cat or 'math' in cat:
                firstlast += 1
    ans['years'] = dict(peer_years.items())
    ans['notreviewedyears'] = dict(other_years.items())
    ans['pr'] = sum(map(len,peer_years.values()))
    ans['npr'] = sum(map(len,other_years.values()))
    ans['firstlast'] = firstlast

    ans['updated'] = date.today().strftime("%B %Y")

    return ans

    
def boldnke(s):
    return re.sub("N. Eriksson", r"\\textbf{N. Eriksson}", s)

def tolatex(string):
    #replace <i></i> with \textit{ }
    s2 = re.sub("<i>", r"\\textit{", string)
    s3 = re.sub("</i>", "}", s2)
    return s3

LATEX_SUBS = (
    #(re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

def main():
    context = parse_yaml('../source/_paper_data.yaml')
    latex_jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(['.']), 
        block_start_string = '\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\VAR{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        line_statement_prefix = '%-',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
    )
    latex_jinja_env.filters["htmltolatex"] = tolatex
    latex_jinja_env.filters["boldnke"] = boldnke
    latex_jinja_env.filters["escapetex"] = escape_tex

    template = latex_jinja_env.get_template('template.tex')
    with open('cv.tex', 'w') as fp:
        fp.write(template.render(context))

if __name__ == '__main__':
    main()
