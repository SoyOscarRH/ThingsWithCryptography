import React, { FunctionComponent } from "react"
import ReactDOM from "react-dom"

import GenerateKeys from "./GenerateKeys"
import Header from "./Header"
import Buttons from "./Buttons"
import Encrypt from "./Encrypt"
import Decrypt from "./Decrypt"
import Footer from "./Footer"


const App: FunctionComponent = () => {
  return (
    <>
      <Header />

      <main className="container" style={{ minHeight: "85vh" }}>
        <section style={{ padding: "3rem", paddingLeft: "0rem" }}>
          <h2>Hybrid</h2>
          <p>Click on the button to display the respective content.</p>
        </section>

        <Buttons />
        <GenerateKeys />

        <Encrypt />
        <Decrypt />
      </main>

      <Footer />
    </>
  )
}

const DOMNode = document.getElementById("ReactApp")
ReactDOM.render(<App />, DOMNode)
