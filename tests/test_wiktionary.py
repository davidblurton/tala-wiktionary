import pytest

from wiktionary import Wiktionary, Declensions

wiktionary = Wiktionary('hestur.xml')

def test_database_discovers_templates():
  assert wiktionary.get_declension_template('kk sb 01') is not None

def test_page_title():
  page = wiktionary.get_by_title('hestur')
  assert page.name == 'hestur'

def test_page_declension_arguments():
  page = wiktionary.get_by_title('hestur')
  assert page.declension_arguments[0] == 'hest'
  assert page.declension_arguments[1] == 'ur'

def test_page_part_of_speech():
  page = wiktionary.get_by_title('hestur')
  assert page.category == 'nafnorð'

def test_page_part_of_speech():
  page = wiktionary.get_by_title('hestur')
  assert page.part_of_speech == 'kk'

def test_page_is_icelandic():
  page = wiktionary.get_by_title('hestur')
  assert page.is_icelandic == True

def test_get_declension_templates():
  templates = Declensions(wiktionary).get_declension_templates('kk sb 01')

  assert len(templates) >= 16
  assert templates[0] == '[[{{{lo.nf.et.ó|}}} {{{1}}}{{{2}}}]] {{{no|}}}'

def test_declensions():
  declensions = Declensions(wiktionary).get_declensions('hestur')

  assert len(declensions) == 16
  assert declensions[1] == dict(name='hesturinn', grammar_tag='lo.nf.et.á')
