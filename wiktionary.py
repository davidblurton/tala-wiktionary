import xml.etree.ElementTree as ET
import wikitextparser as wtp

from wikiexpand.expand import ExpansionContext
from wikiexpand.expand.templates import TemplateDict


NOUN_TEMPLATES = (
    "-is-nafnorð-",
    "-is-sérnafn-",
    "-is-örnefni-",
    "-is-karlmannsnafn-",
    "-is-kvenmannsnafn-",
)


class Page:
    def __init__(self, page, ns):
        self.page = page
        self.ns = ns

    @property
    def title(self):
        return self.page.find("ns:title", self.ns).text

    @property
    def body(self):
        return self.page.find("ns:revision", self.ns).find("ns:text", self.ns).text

    @property
    def templates(self):
        if self.body:
            parsed = wtp.parse(self.body)
            return parsed.templates

    def get_entries(self):
        if self.body and self.templates:
            # TODO: Handle pages with multiple entries
            yield Entry(self.title, self.templates)


class Entry:
    def __init__(self, title, templates):
        self.name = title
        self.templates = templates

    @property
    def declension_group(self):
        t = next(
            iter((t for t in self.templates if t.name.startswith("Fallbeyging"))), None
        )

        if t is not None:
            return t.name.replace("Fallbeyging ", "").strip()

    @property
    def declension_arguments(self):
        t = next(
            iter((t for t in self.templates if t.name.startswith("Fallbeyging"))), None
        )

        if t is not None:
            return [a.value for a in t.arguments]

    @property
    def part_of_speech(self):
        for template in self.templates:
            if template.name.startswith(('Fallbeyging kk sb', 'Fallbeyging kk vb')):
                return 'Karlkynsnafnorð'
            if template.name.startswith(('Fallbeyging kvk sb', 'Fallbeyging kvk vb')):
                return 'Kvenkynsnafnorð'
            if template.name.startswith(('Fallbeyging hk sb', 'Fallbeyging hk vb')):
                return 'Hvorugkynsnafnorð'

    @property
    def category(self):
        for template in self.templates:
            if template.name in NOUN_TEMPLATES:
                return template.name.replace("-is-", "").replace("-", "")

        return "" # XXX: Default category?

    @property
    def is_icelandic(self):
        for template in self.templates:
            if template.name == "-is-":
                return True

        return False

    @property
    def translations(self):
        for template in self.templates:
            if template.name == "þýðing":
                yield dict(
                    lang=template.arguments[0].value,
                    meaning=template.arguments[1].value,
                )

            if template.name == "þýðing-xx":
                yield dict(
                    lang=template.arguments[0].value,
                    meaning=template.arguments[1].value,
                )
                yield dict(
                    lang=template.arguments[0].value,
                    meaning=template.arguments[2].value,
                )

    def to_dict(self):
        return dict(
            name=self.name,
            part_of_speech=self.part_of_speech,
            category=self.category,
            declension_group=self.declension_group,
        )

    def __repr__(self):
        return "<Entry(name=%s)>" % (self.name)


class Wiktionary:
    def __init__(self, xml_file):
        ns = {"ns": "http://www.mediawiki.org/xml/export-0.10/"}
        articles = ET.parse(xml_file)
        pages = articles.getroot().iter(
            "{http://www.mediawiki.org/xml/export-0.10/}page"
        )

        pages = [Page(page, ns) for page in pages]

        self.pages_by_title = {}
        self.declension_templates = {}

        for page in pages:
            self.pages_by_title[page.title] = page

            if page.title.startswith("Snið:Fallbeyging"):
                decl = page.title.replace("Snið:Fallbeyging", "").strip()
                self.declension_templates[decl] = page

    @property
    def pages(self):
        return self.pages_by_title.values()

    def get_by_title(self, title):
        return self.pages_by_title[title]

    def get_declension_template(self, title):
        return self.declension_templates[title]


class Declensions:
    def __init__(self, database):
        self.db = database

    def get_declension_templates(self, declension):
        templ = self.db.get_declension_template(declension)

        declensions = []

        for a in templ.templates[0].arguments:
            val = a.value.strip()

            if "{{{" in val:
                declensions.append(val)

        return declensions

    def get_declensions(self, word):
        page = self.db.get_by_title(word)
        entry = next(page.get_entries())

        templates = self.get_declension_templates(entry.declension_group)
        declension_args = entry.declension_arguments

        results = []
        tpl = TemplateDict()
        ctx = ExpansionContext(templates=tpl)

        for template in templates:
            parsed = wtp.parse(template)
            grammar_tag = parsed.parameters[0].name

            args = {str(i + 1): val for i, val in enumerate(entry.declension_arguments)}
            expanded = ctx.expand(template, args)

            cleaned = str(expanded).replace("[[", "").replace("]]", "").strip()

            if cleaned != "":
                results.append(dict(grammar_tag=grammar_tag, name=cleaned))

        return results
