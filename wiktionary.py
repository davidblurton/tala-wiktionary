import xml.etree.ElementTree as ET
import wikitextparser as wtp

from wikiexpand.expand import ExpansionContext
from wikiexpand.expand.templates import TemplateDict
from utils import cached_property


NOUN_TEMPLATES = ('-is-nafnorð-', '-is-sérnafn-', '-is-örnefni-', '-is-karlmannsnafn-', '-is-kvenmannsnafn-')


class Page:
  def __init__(self, page, ns):
    self.page = page
    self.ns = ns

  @cached_property
  def name(self):
    return self.page.find('ns:title', self.ns).text

  @cached_property
  def body(self):
    return self.page.find('ns:revision', self.ns).find('ns:text', self.ns).text

  @cached_property
  def parsed(self):
    if self.body:
      return wtp.parse(self.body)

  @cached_property
  def declension(self):
    parsed = self.parsed

    if parsed:
      t = next(iter((t for t in parsed.templates if t.name.startswith('Fallbeyging'))), None)

      if t is not None:
        return t.name.replace('Fallbeyging ', '').strip()

  @cached_property
  def declension_arguments(self):
    parsed = self.parsed

    if parsed:
      t = next(iter((t for t in parsed.templates if t.name.startswith('Fallbeyging'))), None)

      if t is not None:
        return [a.value for a in t.arguments]

  @cached_property
  def part_of_speech(self):
    templates = self.parsed.templates

    for index, template in enumerate(templates):
      if template.name in NOUN_TEMPLATES:
        return templates[index + 1].name.replace('.', '')

  @cached_property
  def category(self):
    templates = self.parsed.templates

    for template in templates:
      if template.name in NOUN_TEMPLATES:
        return template.name.replace('-is-', '').replace('-', '')

  @cached_property
  def is_icelandic(self):
    if self.parsed.templates:
      for template in self.parsed.templates:
        if template.name == '-is-':
          return True

    return False

  @cached_property
  def translations(self):
    if self.parsed.templates:
      for template in self.parsed.templates:
        if template.name == 'þýðing':
          yield dict(lang=template.arguments[0].value, meaning=template.arguments[1].value)

        if template.name == 'þýðing-xx':
          yield dict(lang=template.arguments[0].value, meaning=template.arguments[1].value)
          yield dict(lang=template.arguments[0].value, meaning=template.arguments[2].value)

  def to_dict(self):
    return dict(name=self.name, part_of_speech=self.part_of_speech, category=self.category)

  def __repr__(self):
    return '<Page(name=%s)>' % (self.name)


class Wiktionary:
  def __init__(self, xml_file):
    ns = {'ns': 'http://www.mediawiki.org/xml/export-0.10/'}
    articles = ET.parse(xml_file)
    pages = articles.getroot().iter('{http://www.mediawiki.org/xml/export-0.10/}page')

    pages = [Page(page, ns) for page in pages]

    self.pages_by_title = {}
    self.declension_templates = {}

    for page in pages:
      self.pages_by_title[page.name] = page

      if page.name.startswith('Snið:Fallbeyging'):
        decl = page.name.replace('Snið:Fallbeyging', '').strip()
        self.declension_templates[decl] = page

  @property
  def pages(self):
    return self.pages_by_title.values()

  def get_by_title(self, name):
    return self.pages_by_title[name]

  def get_declension_template(self, name):
    return self.declension_templates[name]


class Declensions:
  def __init__(self, database):
    self.db = database

  def get_declension_templates(self, declension):
    templ = self.db.get_declension_template(declension)

    declensions = []

    for a in templ.parsed.templates[0].arguments:
      val = a.value.strip()

      if '{{{' in val:
        declensions.append(val)

    return declensions


  def get_declensions(self, word):
    page = self.db.get_by_title(word)

    templates = self.get_declension_templates(page.declension)
    declension_args = page.declension_arguments

    results = []
    tpl = TemplateDict()
    ctx = ExpansionContext(templates=tpl)

    for template in templates:
      parsed = wtp.parse(template)
      grammar_tag = parsed.parameters[0].name

      args = {str(i + 1):val for i, val in enumerate(page.declension_arguments)}
      expanded = ctx.expand(template, args)

      cleaned = str(expanded).replace('[[', '').replace(']]', '').strip()

      if cleaned != '':
        results.append(dict(grammar_tag=grammar_tag, name=cleaned))

    return results

  def print_declensions(self, declensions):
    col_count = len(declensions) // 4

    row_format ="{:<15}" * col_count
    for g in zip(*(iter(declensions),) * col_count):
      print(row_format.format(*g))


# db = Wiktionary('articles.xml')

# def pp(word):
#   try:
#     page = db.get_by_title(word)
#     templ = db.get_declension_template(page.declension)

#     d = Declensions()
#     d.print_declensions(d.get_declensions(page, templ))
#   except KeyError:
#     print('{} not found'.format(word))
