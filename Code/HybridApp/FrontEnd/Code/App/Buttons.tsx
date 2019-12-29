import React, { FunctionComponent as FC, useState } from "react"

const Button: FC<{ type: string; target: string; name: string }> = ({ type, name, target }) => {
  const [isOn, change] = useState(false)
  const toggle = () => change(!isOn)

  return (
    <button
      type="button"
      style={{ height: "3.5rem" }}
      className={`btn btn${!isOn ? "-outline" : ""}-${type}`}
      data-toggle="collapse"
      data-target={target}
      onClick={toggle}
    >
      {name}
    </button>
  )
}

const Buttons: FC = () => {
  const style = {
    display: "grid",
    gridAutoFlow: "column",
    gridGap: "1rem",
    marginBottom: "2rem",
    overflow: "scroll",
  }

  return (
    <section style={style}>
      <Button target="#Key" type="primary" name="Key Generator" />
      <Button target="#Encrypt" type="success" name="Encrypt" />
      <Button target="#Decrypt" type="danger" name="Decrypt" />
    </section>
  )
}

export default Buttons
