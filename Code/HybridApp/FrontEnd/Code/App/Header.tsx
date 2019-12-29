import React, { FunctionComponent } from "react"

const Header: FunctionComponent = () => {
  return (
    <nav className="navbar navbar-expand-sm bg-dark navbar-dark" style={{height: "60px"}}>
      <ul className="navbar-nav">
        <li className="nav-item active">
          <a style={{color: "white", fontSize: "20px"}}>Hybrid Encryption</a>
        </li>
      </ul>
    </nav>
  )
}

export default Header