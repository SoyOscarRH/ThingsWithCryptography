import React, { FunctionComponent, useState } from "react"
import { saveFile } from "./Helpers"

import FormInput from "./FormInput"

const headers = { Accept: "application/json", "Content-Type": "application/json" }

const Encrypt: FunctionComponent = () => {
  const [fromKeys, changeFrom] = useState<Record<string, string>>({})
  const [toKeys, changeTo] = useState<Record<string, string>>({})
  const [text, changeText] = useState("")
  const [name, changeName] = useState("")

  const [doingStuff, changeDoing] = useState(true)
  const [doingSign, changeSign] = useState(true)
  const [isLoading, changeLoading] = useState(false)

  const getText = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files && event.target.files[0]
    if (!file) return

    // @ts-ignore
    changeText(await file.text())
    changeName(file.name.split(".", 1)[0])
  }

  const getKeys = async (event: React.ChangeEvent<HTMLInputElement>, change) => {
    const file = event.target.files && event.target.files[0]
    if (!file) return

    // @ts-ignore
    const text = await file.text()
    try {
      change(JSON.parse(text))
    } catch (error) {
      alert("This is not a valid key file")
    }
  }


  

  const callToCipher = async () => {
    changeLoading(true)
    const url = "/createCipher"
    const body = JSON.stringify({
      OPE: toKeys.GFD,
      YEE: toKeys.BCD,
      PQE: fromKeys.GFD,
      PEE: fromKeys.BCD,
      ABW: text,
      SHJ: doingStuff,
      SKQ: doingSign,
    })


    const response = await fetch(url, { headers, method: "POST", body })
    const keysResponse = await response.json()

    if (keysResponse.error) {
      alert(keysResponse.error)
      changeLoading(false)
      return
    }

    const { DAF, BCD, GFA, CGB } = keysResponse
    const load = { DAF, BCD, GFA, CGB }
    changeLoading(false)

    saveFile(`${name}.cipher`, JSON.stringify(load))
  }

  return (
    <section id="Encrypt" className="collapse"  style={{ maxWidth: "400px" }}>
      <p>We need many things:</p>

      <div className="checkbox">
        <label>
          <input
            type="checkbox"
            checked={doingStuff}
            onChange={() => changeDoing(e => !e)}
            data-toggle="toggle"
          />
          Confidentiality
        </label>
      </div>
      <div className="checkbox">
        <label>
          <input
            type="checkbox"
            checked={doingSign}
            onChange={() => changeSign(e => !e)}
            data-toggle="toggle"
          />
          Authentication
        </label>
      </div>

      {doingSign && (
        <FormInput onChange={e => getKeys(e, i => changeFrom(i))} name="From Keys (private)" />
      )}

      {doingStuff && (
        <FormInput onChange={e => getKeys(e, i => changeTo(i))} name="To Keys (public)" />
      )}

      <FormInput onChange={getText} name="Text" loading={isLoading} onClick={callToCipher} />
    </section>
  )
}

export default Encrypt
