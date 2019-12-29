import React, { StrictMode, FunctionComponent, useState, useRef } from "react"
import ReactDOM from "react-dom"

import { Button } from "@material-ui/core/"

import { Modes, MyButton } from "./Modes"
import { Section } from "./Style"

const App: FunctionComponent = () => {
  const [doIt, changeDo] = useState("encrypt")
  const [mode, changeMode] = useState("ECB")
  const [algo, changeAlgo] = useState("DES")
  const [url, changeURL] = useState("")
  const [urlOutput, changeURLOutput] = useState("")
  const formRef = useRef()

  const updateStuff = async (file: File) => {
    const formData = new FormData()
    formData.append("file", file, file.name)
    formData.append("mode", mode)
    formData.append("algo", algo)
    formData.append("do", doIt)

    changeURL(URL.createObjectURL(file))

    try {
      const response = await fetch("/", { body: formData, method: "post" })
      const json = await response.json()

      changeURLOutput(json.path)

      console.log(json)
    } catch (e) {
      console.log(e)
    }
  }

  return (
    <div style={Section}>
      <section>
        <h2>
          Operation Mode: {mode} - {algo}
        </h2>
      </section>

      <section>
        <h3>Select algorithm:</h3>

        <div style={{ display: "grid", gridGap: "1rem", gridAutoFlow: "column" }}>
          {["AES", "DES"].map(thisAlgo => (
            <MyButton
              key={thisAlgo}
              onClick={() => changeAlgo(thisAlgo)}
              isFull={algo === thisAlgo}
              mini={thisAlgo}
              title={""}
            />
          ))}
        </div>

        <h3>Select thing to do:</h3>

        <div style={{ display: "grid", gridGap: "1rem", gridAutoFlow: "column" }}>
          {["encrypt", "decrypt"].map(doThis => (
            <MyButton
              key={doThis}
              onClick={() => changeDo(doThis)}
              isFull={doIt === doThis}
              mini={doThis}
              title={""}
            />
          ))}
        </div>

        <h3>Select mode:</h3>

        <div style={{ display: "grid", gridGap: "1rem", gridTemplateColumns: "1fr 1fr" }}>
          {Modes.map(({ mini, title }) => (
            <MyButton
              key={mini}
              onClick={() => changeMode(mini)}
              isFull={mode === mini}
              mini={mini}
              title={title}
            />
          ))}
        </div>

        <br />
        <br />

        <Button
          onClick={() => {
            formRef &&
              formRef.current &&
              formRef.current.firstChild &&
              formRef.current.firstChild.files &&
              formRef.current.firstChild.files[0] &&
              updateStuff(formRef.current.firstChild.files[0])
          }}
          style={{ height: "4rem" }}
          size="medium"
          variant={"contained"}
          color="primary"
        >
          Do it
        </Button>
      </section>

      <section>
        <form method="post" action="" id="login" ref={formRef} style={{ textAlign: "center" }}>
          <input
            type="file"
            onChange={event => {
              const file = event.target.files && event.target.files[0]
              if (!file) return

              updateStuff(file)
            }}
          />
          <br />
          <br />
          <br />
          <section
            style={{
              textAlign: "center",
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gridGap: "1rem",
            }}
          >
            <div>
              {url && <h3>Input</h3>}
              <img style={{ display: "block", margin: "auto auto" }} src={url} width="100%" />
            </div>

            <div>
              {urlOutput && <h3>Output</h3>}
              <img style={{ display: "block", margin: "auto auto" }} src={urlOutput} width="100%" />
            </div>
          </section>
        </form>
      </section>
    </div>
  )
}

const DOM_NODE = document.getElementById("ReactApp")
ReactDOM.render(
  <StrictMode>
    <App />
  </StrictMode>,
  DOM_NODE
)
