import React from "react"
import { Button } from "@material-ui/core/"
import NavigationIcon from "@material-ui/icons/Navigation"

const Modes = [
  { mini: "ECB", title: "Electronic codebook" },
  { mini: "CBC", title: "Cipher block chaining" },
  { mini: "OFB", title: "Cipher output Feeback" },
  { mini: "CFB", title: "Cipher Feedback Mode" },
]

const MyButton = ({ onClick, isFull, title, mini }) => (
  <Button
    onClick={onClick}
    variant={isFull ? "contained" : "outlined"}
    style={{ height: "3rem" }}
    size="medium"
    color="primary"
  >
    <NavigationIcon />
    <b>{mini}{title && ":"}</b> {title}
  </Button>
)

export { Modes, MyButton }
