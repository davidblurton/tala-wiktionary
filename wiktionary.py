import xml.etree.ElementTree as ET
import wikitextparser as wtp

from wikiexpand.expand import ExpansionContext
from wikiexpand.expand.templates import TemplateDict


class cached_property(object):
    """
    Descriptor (non-data) for building an attribute on-demand on first use.
    """
    def __init__(self, factory):
        """
        <factory> is called such: factory(instance) to build the attribute.
        """
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        # Build the attribute.
        attr = self._factory(instance)

        # Cache the value; hide ourselves.
        setattr(instance, self._attr_name, attr)

        return attr


NOUN_TEMPLATES = ('-is-nafnorð-', '-is-sérnafn-', '-is-örnefni-', '-is-karlmannsnafn-', '-is-kvenmannsnafn-')


class Entry:
  def __init__(self, page, ns):
    self.page = page
    self.ns = ns

  @cached_property
  def title(self):
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
  def is_icelandic(self):
    if self.parsed.templates:
      return self.parsed.templates[0].name == '-is-'

    return False

  def __repr__(self):
    return '<Entry(title=%s)>' % (self.title)


class Database:
  def __init__(self, xml_file):
    ns = {'ns': 'http://www.mediawiki.org/xml/export-0.10/'}
    articles = ET.parse(xml_file)
    pages = articles.getroot().iter('{http://www.mediawiki.org/xml/export-0.10/}page')

    entries = [Entry(page, ns) for page in pages]

    self.entries = entries

    self.entries_by_title = {}
    self.declension_templates = {}

    for e in entries:
      self.entries_by_title[e.title] = e

      if e.title.startswith('Snið:Fallbeyging'):
        decl = e.title.replace('Snið:Fallbeyging', '').strip()
        self.declension_templates[decl] = e

  def get_by_title(self, title):
    return self.entries_by_title[title]

  def get_declension_template(self, name):
    return self.declension_templates[name]


class Declensions:
  def __init__(self, database):
    self.db = database

  def get_declensions(self, word):
    try:
      entry = self.db.get_by_title(word)
      templ = self.db.get_declension_template(entry.declension)

      declension_args = entry.declension_arguments
      declensions = []

      for a in templ.parsed.templates[0].arguments:
        val = a.value.strip()

        if '{{{' in val:
          declensions.append(val)

      results = []
      tpl = TemplateDict()
      ctx = ExpansionContext(templates=tpl)

      for decl in declensions:
        args = {str(i + 1):val for i, val in enumerate(entry.declension_arguments)}
        expanded = ctx.expand(decl, args)

        cleaned = str(expanded).replace('[[', '').replace(']]', '').strip()

        if cleaned != '':
          results.append(cleaned)

      return results
    except Exception as exc:
      raise Exception('Failed to get declensions for {}'.format(word))

  def print_declensions(self, declensions):
    col_count = len(declensions) // 4

    row_format ="{:<15}" * col_count
    for g in zip(*(iter(declensions),) * col_count):
      print(row_format.format(*g))


# db = Database('articles.xml')

# def pp(word):
#   try:
#     entry = db.get_by_title(word)
#     templ = db.get_declension_template(entry.declension)

#     d = Declensions()
#     d.print_declensions(d.get_declensions(entry, templ))
#   except KeyError:
#     print('{} not found'.format(word))
