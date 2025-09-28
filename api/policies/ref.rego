package rainref.allow

default allow = false

allow {
  input.action.type == "resend_activation"
}
