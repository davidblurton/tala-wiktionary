import React from "react";
import styles from "./styles.module.css";

import Table from "../Table";

const columns = [
  {
    header: "Eintala",
    render: data => data[0].map(form => form.name)
  },
  {
    header: "Fleirtala",
    render: data => data[1].map(form => form.name)
  }
];

export default ({ lemma, query, withArticle = false }) => (
  <div className={styles.root}>
    <div className={styles.lemmaName}>{lemma.name}</div>
    <div className={styles.partOfSpeech}>{lemma.partOfSpeech}</div>

    <div className={styles.translations}>
      {lemma.translations.map(translation => (
        <div className={styles.translation}>
          <div className={styles.definition}>{translation.lang}</div>
          <div>{translation.meaning}</div>
        </div>
      ))}
    </div>

    <div className={styles.forms}>
      {lemma.forms &&
        [0, 2]
          .map(i => (withArticle ? i + 1 : i))
          .filter(i => i < lemma.forms.length)
          .map(index => lemma.forms[index])
          .map(group => (
            <div className={styles.formGroup}>
              {group.map(form => (
                <div className={styles.form}>
                  <span className={form.name === query ? styles.formMatch : undefined}>
                    {form.name}
                  </span>
                </div>
              ))}
            </div>
          ))}
    </div>

    {/* <Table columns={columns} data={lemma.forms} /> */}
  </div>
);
