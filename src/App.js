import React, { Component } from "react";
import { Query } from "react-apollo";
import gql from "graphql-tag";
import createHistory from "history/createBrowserHistory";

import "./App.css";
import "typeface-roboto-slab";

import Logo from "./Components/Logo";
import Search from "./Components/Search";
import Lemma from "./Components/Lemma";

const history = createHistory();

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
    searchValue: history.location.pathname.slice(1)
  };

  handleSearch = event => {
    history.replace({
      pathname: `/${event.target.value}`
    });
  };

  componentDidMount() {
    history.listen((location, action) => {
      this.setState({
        searchValue: location.pathname.slice(1)
      });
    });
  }

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

        <div className="App-footer">
          <div className="App-source">
            <p>Gögnin frá <a href="https://is.wiktionary.org/wiki/Wikior%C3%B0ab%C3%B3k:Fors%C3%AD%C3%B0a">Wikiorðabókinni</a>.</p>
            <p><a href="https://tala.is">tala.islensku</a> er verkefni eftir <a href="http://davidblurton.com">David Blurton</a>.</p>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
