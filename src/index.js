import React from "react";
import ReactDOM from "react-dom";
import initReactFastclick from 'react-fastclick';
import { ApolloProvider } from "react-apollo";

import * as serviceWorker from "./serviceWorker";
import client from "./client";
import App from "./App";

import "./index.css";

initReactFastclick();

const Index = () => (
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>
);

ReactDOM.render(<Index />, document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
