import json

import click
from graphql import graphql

from gql.schema import schema


@click.command()
@click.option("-f", "--filename", default="src/schema.json", help="The output file name")
def export(filename):
    introspection = graphql(
        schema,
        """
      {
        __schema {
          types {
            kind
            name
            possibleTypes {
              name
            }
          }
        }
      }""",
    )

    with open(filename, "w") as f:
        f.write(json.dumps(introspection.data, indent=2, sort_keys=True, separators=(",", ": ")))


if __name__ == "__main__":
    export()
