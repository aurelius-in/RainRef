package rainref.allow

default allow = {"allow": false, "reason": "not allowed"}

allow = res {
  some t
  t := input.action.type
  res := {"allow": allowed_action[t], "reason": reason_for[t]}
}

allowed_action := {
  "resend_activation": true
}

reason_for := {
  "resend_activation": "policy: resend activation allowed"
}
