from flask import Flask
from flask_cors import CORS

from flask_graphql import GraphQLView
from gql.schema import schema

app = Flask(__name__)
CORS(app)


app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


@app.route("/")
def hello_world():
    return "tala.is graphql server"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
