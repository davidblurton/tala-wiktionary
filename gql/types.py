import graphene
import models


class GrammarCase(graphene.Enum):
    nominative = "nominative"
    accusative = "accusative"
    dative = "dative"
    genitive = "genitive"


class GrammarNumber(graphene.Enum):
    singular = "singular"
    plural = "plural"


class GrammarArticle(graphene.Enum):
    indefinite = "indefinite"
    definite = "definite"


class Grammar(graphene.ObjectType):
    case = graphene.Field(GrammarCase)
    number = graphene.Field(GrammarNumber)
    article = graphene.Field(GrammarArticle)

    def resolve_case(form, info):
        if "nf" in form.grammar_tag:
            return GrammarCase.nominative
        if "þf" in form.grammar_tag:
            return GrammarCase.accusative
        if "þgf" in form.grammar_tag:
            return GrammarCase.dative
        if "ef" in form.grammar_tag:
            return GrammarCase.genitive

    def resolve_number(form, info):
        if "et" in form.grammar_tag:
            return GrammarNumber.singular
        if "ft" in form.grammar_tag:
            return GrammarNumber.plural

    def resolve_article(form, info):
        if "ó" in form.grammar_tag:
            return GrammarArticle.indefinite
        if "á" in form.grammar_tag:
            return GrammarArticle.definite


class Form(graphene.ObjectType):
    name = graphene.String()
    lemma = graphene.Field(lambda: Lemma)
    grammar_tag = graphene.String()
    grammar = graphene.Field(Grammar)

    def resolve_grammar(form, info):
        return form


class Lemma(graphene.ObjectType):
    name = graphene.String()
    category = graphene.String()
    part_of_speech = graphene.String()
    declension_group = graphene.String()
    forms = graphene.List(graphene.List(lambda: Form))
    translations = graphene.List(lambda: Translation, lang=graphene.String())

    def resolve_forms(lemma, info):
        forms = lemma.forms

        group_size = len(forms) // 4
        grouped = zip(*(iter(forms),) * group_size)

        return list(map(list, zip(*grouped)))

    def resolve_translations(lemma, info, lang=None):
        if not lang:
            return lemma.translations

        return lemma.translations.select().filter(models.Translation.lang == lang)


class Translation(graphene.ObjectType):
    lang = graphene.String()
    meaning = graphene.String()
    lemma = graphene.Field(lambda: Lemma)

    def resolve_forms(translation, info):
        return translation.lemma


TYPES = [Form, Lemma]
