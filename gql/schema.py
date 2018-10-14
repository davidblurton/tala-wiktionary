import graphene

from gql.types import TYPES
from gql.query import Query

schema = graphene.Schema(query=Query, types=TYPES)
