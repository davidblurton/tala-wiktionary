import React from "react";

import styles from "./styles.module.css";

export default ({ columns, data }) => (
  <div className={styles.table}>
    {columns.map(col => (
      <div>{col.header}</div>
    ))}

    {columns.map(col => (
      <div>{col.render(data)}</div>
    ))}
  </div>
);
