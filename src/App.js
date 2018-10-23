import React, { Component } from "react";
import { Query } from "react-apollo";
import gql from "graphql-tag";

import "./App.css";
import "typeface-roboto-slab";

import Logo from "./Components/Logo";
import Search from "./Components/Search";
import Lemma from "./Components/Lemma";

const SearchQuery = gql`
  query SearchQuery($query: String) {
    search(query: $query, uniqueLemma: true) {
      __typename
      ... on Lemma {
        ...LemmaFields
      }
      ... on Form {
        lemma {
          ...LemmaFields
        }
      }
      ... on Translation {
        lang
        meaning
        lemma {
          ...LemmaFields
        }
      }
    }
  }

  fragment LemmaFields on Lemma {
    __typename
    name
    partOfSpeech
    declensionGroup
    forms {
      __typename
      name
    }
    translations(lang: "en") {
      __typename
      lang
      meaning
    }
  }
`;

class App extends Component {
  state = {
    searchValue: "hestur"
  };

  handleSearch = event => {
    this.setState({
      searchValue: event.target.value
    });
  };

  render() {
    const { searchValue } = this.state;

    return (
      <div className="App">
        <div className="App-content">
          <div className="App-logo">
            <Logo />
          </div>

          <Search
            value={searchValue}
            onChange={this.handleSearch}
            placeholder="Leita að orði"
          />

          <Query
            query={SearchQuery}
            variables={{ query: searchValue }}
            skip={!searchValue}
          >
            {({ loading, error, data }) => {
              if (error) return <p>Error :(</p>;

              if (!data) {
                return null;
              }

              if (!data.search) {
                return null;
              }

              return data.search.map((result, i) => (
                <div key={i}>
                  {result.__typename === "Lemma" && (
                    <Lemma lemma={result} query={searchValue} />
                  )}
                  {result.__typename === "Form" && (
                    <Lemma lemma={result.lemma} query={searchValue} />
                  )}
                  {result.__typename === "Translation" && (
                    <Lemma lemma={result.lemma} query={searchValue} />
                  )}
                </div>
              ));
            }}
          </Query>
        </div>
      </div>
    );
  }
}

export default App;
