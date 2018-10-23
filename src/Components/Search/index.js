import React from "react";
import styles from "./styles.module.css";

export default ({ value, onChange, placeholder }) => (
  <input
    className={styles.input}
    value={value}
    onChange={onChange}
    placeholder={placeholder}
    autoCapitalize="none"
  />
);
