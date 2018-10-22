import responder

from flask import Flask

from flask_graphql import GraphQLView
from gql.schema import schema

api = responder.API()
app = Flask(__name__)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

# api.add_route("/graphql", schema)

@app.route("/")
def hello_world():
    return "tala.is graphql server"


if __name__ == "__main__":
    api.run(port=5000)
