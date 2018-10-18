import pytest

from wiktionary import Wiktionary, Declensions

wiktionary = Wiktionary("tests/hestur.xml")
page = wiktionary.get_by_title("hestur")
entry = next(page.get_entries())


def test_database_discovers_templates():
    assert wiktionary.get_declension_template("kk sb 01") is not None


def test_entry_title():
    assert entry.name == "hestur"


def test_entry_declension_arguments():
    assert entry.declension_arguments[0] == "hest"
    assert entry.declension_arguments[1] == "ur"


def test_entry_part_of_speech():
    assert entry.category == "nafnorð"


def test_entry_part_of_speech():
    assert entry.part_of_speech == "kk"


def test_entry_is_icelandic():
    assert entry.is_icelandic == True


def test_entry_translations():
    translations = list(entry.translations)
    translations_by_lang = {t["lang"]: t["meaning"] for t in translations}

    assert (
        len(translations) == 16
    )  # XXX: There are multiple translations for some languages
    assert translations_by_lang["en"] == "horse"


def test_get_declension_templates():
    templates = Declensions(wiktionary).get_declension_templates("kk sb 01")

    assert len(templates) >= 16
    assert templates[0] == "[[{{{lo.nf.et.ó|}}} {{{1}}}{{{2}}}]] {{{no|}}}"


def test_declensions():
    declensions = Declensions(wiktionary).get_declensions("hestur")

    assert len(declensions) == 16
    assert declensions[1] == dict(name="hesturinn", grammar_tag="lo.nf.et.á")
