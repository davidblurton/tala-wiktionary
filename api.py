import responder

from gql.schema import schema

api = responder.API(static_dir='build')

api.add_route("/graphql", schema)
# api.add_route("/", static=True)

@api.route("/")
async def frontend(req, resp):
    resp.content = api.static_response(req, resp)

if __name__ == "__main__":
    api.run(address='0.0.0.0', port=5000)
