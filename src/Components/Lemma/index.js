import React from "react";
import styles from "./styles.module.css";
import {groupBy} from 'lodash';

// import Table from "../Table";
//
// const columns = [
//   {
//     header: "Eintala",
//     render: data => data[0].map(form => form.name)
//   },
//   {
//     header: "Fleirtala",
//     render: data => data[1].map(form => form.name)
//   }
// ];

Array.prototype.flatMap = function(lambda) {
  return Array.prototype.concat.apply([], this.map(lambda));
};

export default class Lemma extends React.PureComponent {
  state = {
    withArticle: false
  };

  toggleWithArticle = () => {
    this.setState({
      withArticle: !this.state.withArticle
    });
  };

  componentDidMount() {
    const { lemma, query } = this.props;

    const forms = [1, 3]
      .filter(i => i < lemma.forms.length)
      .map(index => lemma.forms[index])
      .flatMap(x => x)
      .map(lemma => lemma.name);

    if (forms.includes(query)) {
      this.setState({
        withArticle: true
      });
    }
  }

  render() {
    const { lemma, query } = this.props;
    const { withArticle } = this.state;

    const translationsByLang = groupBy(lemma.translations, 'lang')

    return (
      <div className={styles.root}>
        <div className={styles.lemmaName}>{lemma.name}</div>
        <div className={styles.partOfSpeech}>
          {lemma.partOfSpeech}
          <span className={styles.declensionGroup}>
            {lemma.declensionGroup.includes("sb") && " sterk beyging"}
            {lemma.declensionGroup.includes("vb") && " veik beyging"}
          </span>
        </div>

        <div className={styles.translations}>
          {Object.keys(translationsByLang).map(lang => (
            <div className={styles.translation}>
              <div className={styles.definition}>{lang}</div>
              <div>{translationsByLang[lang].map(translation => translation.meaning).join(', ')}</div>
            </div>
          ))}
        </div>

        <div className={styles.forms}>
          {lemma.forms &&
            [0, 2]
              .map(i => (withArticle ? i + 1 : i))
              .filter(i => i < lemma.forms.length)
              .map(index => lemma.forms[index])
              .map((group, i) => (
                <div className={styles.formGroup}>
                  <div className={styles.tableHeading}>
                    {i == 0 ? "Eintala" : "Fleirtala"}
                  </div>
                  {group.map(form => (
                    <div className={styles.form}>
                      <span
                        className={
                          form.name === query ? styles.formMatch : undefined
                        }
                      >
                        {form.name}
                      </span>
                    </div>
                  ))}
                </div>
              ))}
        </div>

        <div className={styles.toggle} onClick={this.toggleWithArticle}>
          <span className={withArticle ? undefined : styles.formMatch}>
            án greinis
          </span>
          <span> / </span>
          <span className={withArticle ? styles.formMatch : undefined}>
            með greini
          </span>
        </div>

        {/* <Table columns={columns} data={lemma.forms} /> */}

        <div className={styles.footer}>
          <a
            className={styles.footerLink}
            href={`https://is.wiktionary.org/wiki/${lemma.name}`}
          >
            Breyta á wikiorðabóki
          </a>
        </div>
      </div>
    );
  }
}
