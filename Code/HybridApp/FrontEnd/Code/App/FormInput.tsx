import React, { FunctionComponent as FC } from "react"

// eslint-disable-next-line
type fn = any

const FormInput: FC<{ onChange: fn; onClick?: fn; name: string; loading?: boolean }> = props => {
  const { name, onChange, onClick, loading } = props
  const loader = <span className="spinner-grow spinner-grow-sm" aria-hidden="true" />
  const style = { height: "4rem", padding: "1rem" }

  return (
    <div className="input-group mb-3 input-group-sm">
      <div className="input-group-prepend">
        <span className="input-group-text">{name}</span>
      </div>

      <input type="file" className="form-control" onChange={onChange} style={style} />

      {onClick && (
        <div className="input-group-append">
          <button className="btn btn-success" onClick={onClick} disabled={loading}>
            {loading && loader}
            Do it!
          </button>
        </div>
      )}
    </div>
  )
}

export default FormInput
