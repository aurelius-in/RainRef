package rainref.allow

default allow = {"allow": false, "reason": "policy: not allowed"}

# Inputs
# input.action: { type, params, ticket_id? }
# input.user: { roles: [..] }

allow = res {
  some t
  t := input.action.type
  ok := allowed_action(t)
  reason := reason_for[t]
  not ok
  # Override reason with first deny_reason if present when not allowed
  some dr
  dr := deny_reason_first
  reason := dr
  res := {"allow": ok, "reason": reason}
}

allow = res {
  some t
  t := input.action.type
  ok := allowed_action(t)
  ok
  res := {"allow": ok, "reason": reason_for[t]}
}

allowed_action(t) {
  # resend_activation allowed to admin or support_lead
  t == "resend_activation"
  roles := input.user.roles
  roles[_] == "admin"; roles[_] == "support_lead"
}
allowed_action(t) {
  # note allowed to admin, support_lead, or support
  t == "note"
  roles := input.user.roles
  roles[_] == "admin"; roles[_] == "support_lead"
}
allowed_action(t) {
  t == "note"
  roles := input.user.roles
  roles[_] == "support"
}

reason_for := {
  "resend_activation": "policy: resend activation allowed",
  "note": "policy: note allowed",
}

# Admin bypass example (if roles included)
allow = {"allow": true, "reason": "policy: admin bypass"} {
  some roles
  roles := input.user.roles
  roles[_] == "admin"
}

# Deny if missing required param
deny_reason[reason] {
  input.action.type == "resend_activation"
  not input.action.params.user_ref
  reason := "policy: missing user_ref"
}

deny_reason_first := r {
  some rr
  deny_reason[rr]
  r := rr
}
