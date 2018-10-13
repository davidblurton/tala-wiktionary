import pytest

from wiktionary import Wiktionary, Declensions

wiktionary = Wiktionary('hestur.xml')

def test_database_discovers_templates():
  assert wiktionary.get_declension_template('kk sb 01') is not None

def test_entry_title():
  entry = wiktionary.get_by_title('hestur')
  assert entry.title == 'hestur'

def test_entry_declension_arguments():
  entry = wiktionary.get_by_title('hestur')
  assert entry.declension_arguments[0] == 'hest'
  assert entry.declension_arguments[1] == 'ur'

def test_entry_part_of_speech():
  entry = wiktionary.get_by_title('hestur')
  assert entry.category == 'nafnorð'

def test_entry_part_of_speech():
  entry = wiktionary.get_by_title('hestur')
  assert entry.part_of_speech == 'kk'

def test_entry_is_icelandic():
  entry = wiktionary.get_by_title('hestur')
  assert entry.is_icelandic == True

def test_declensions():
  declensions = Declensions(wiktionary).get_declensions('hestur')

  assert len(declensions) == 16
  assert declensions[1] == 'hesturinn'
