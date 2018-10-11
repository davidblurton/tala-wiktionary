from collections import Counter

import xml.etree.ElementTree as ET
import wikitextparser as wtp

from wikiexpand.expand import ExpansionContext
from wikiexpand.expand.templates import TemplateDict

tpl = TemplateDict()
ctx = ExpansionContext(templates=tpl)



class Entry:
  def __init__(self, page, ns):
    self.page = page
    self.ns = ns

    self._title = self.page.find('ns:title', self.ns).text
    self._body = page.find('ns:revision', self.ns).find('ns:text', self.ns).text

  @property
  def title(self):
    return self._title

  @property
  def body(self):
    return self._body

  @property
  def parsed(self):
    if self.body:
      return wtp.parse(self.body)
  
  @property
  def declension(self):
    parsed = self.parsed

    if parsed:
      t = next(iter((t for t in parsed.templates if t.name.startswith('Fallbeyging'))), None)

      if t is not None:
        return t.name.replace('Fallbeyging ', '')

  @property
  def declension_arguments(self):
    parsed = self.parsed

    if parsed:
      t = next(iter((t for t in parsed.templates if t.name.startswith('Fallbeyging'))), None)

      if t is not None:
        return [a.value for a in t.arguments]
  
  
  def __repr__(self):
    return '<Entry(title=%s)>' % (self.title)
    
  
ns = {'ns': 'http://www.mediawiki.org/xml/export-0.10/'}

# page = ET.parse('hestur.xml')

# e = Entry(page)
# print(e.title)

articles = ET.parse('articles.xml')
pages = articles.getroot().iter('{http://www.mediawiki.org/xml/export-0.10/}page')

entries = [Entry(page, ns) for page in pages]

entries_by_title = {}

for e in entries:
  entries_by_title[e.title] = e

declension_templates = {}

for e in entries:
  if e.title.startswith('Snið:Fallbeyging'):
    decl = e.title.replace('Snið:Fallbeyging', '').strip()

    if len(decl) > 3 and not decl.startswith('de ') and not decl.startswith('el-'):
      declension_templates[decl] = e

def get_declensions(word):
  entry = entries_by_title[word]

  declension_args = entry.declension_arguments
  templ = declension_templates[entry.declension]

  declensions = []

  for a in templ.parsed.templates[0].arguments:
    val = a.value.strip()

    if val.startswith('[['):
      declensions.append(val)

  results = []

  for decl in declensions:
    args = {str(i + 1):val for i, val in enumerate(entry.declension_arguments)}
    expanded = ctx.expand(decl, args)
  
    results.append(str(expanded).replace('[[', '').replace(']]', '').strip())

  return results

def print_declensions(declensions):
  col_count = len(declensions) // 4

  row_format ="{:<15}" * col_count
  for g in zip(*(iter(declensions),) * col_count):
    print(row_format.format(*g))

def pp(word):
  try:
    print_declensions(get_declensions(word))
  except KeyError:
    print('{} not found'.format(word))

pp('hestur')
