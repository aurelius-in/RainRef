package rainref.allow

default allow = {"allow": false, "reason": "policy: not allowed"}

# Inputs
# input.action: { type, params, ticket_id? }
# input.user: { roles: [..] }

# Main allow decision with structured reason
allow = res {
  t := input.action.type
  ok := can_run_action(t)
  reason := allow_reason_for[t]
  not ok
  some dr
  dr := first_deny_reason
  reason := dr
  res := {"allow": ok, "reason": reason}
}

allow = res {
  t := input.action.type
  ok := can_run_action(t)
  ok
  res := {"allow": ok, "reason": allow_reason_for[t]}
}

# Role checks per action
can_run_action(t) {
  t == "resend_activation"
  roles := input.user.roles
  roles[_] == "admin"; roles[_] == "support_lead"
}
can_run_action(t) {
  t == "approve_ticket"
  roles := input.user.roles
  roles[_] == "admin"; roles[_] == "support_lead"
}
can_run_action(t) {
  t == "close_ticket"
  roles := input.user.roles
  some r
  r := roles[_]
  r == "admin" or r == "support_lead" or r == "support"
}
can_run_action(t) {
  t == "add_note"
  roles := input.user.roles
  some r
  r := roles[_]
  r == "admin" or r == "support_lead" or r == "support"
}

# Reasons when allowed
allow_reason_for := {
  "resend_activation": "policy: resend activation allowed",
  "approve_ticket": "policy: approve ticket allowed",
  "close_ticket": "policy: close ticket allowed",
  "add_note": "policy: add note allowed",
}

# Admin bypass example
allow = {"allow": true, "reason": "policy: admin bypass"} {
  roles := input.user.roles
  roles[_] == "admin"
}

# Deny reasons: missing params
deny_reason[reason] {
  input.action.type == "resend_activation"
  not input.action.params.user_ref
  reason := "policy: missing user_ref"
}
deny_reason[reason] {
  input.action.type == "approve_ticket"
  not input.action.params.ticket_id
  reason := "policy: missing ticket_id"
}
deny_reason[reason] {
  input.action.type == "close_ticket"
  not input.action.params.ticket_id
  reason := "policy: missing ticket_id"
}
deny_reason[reason] {
  input.action.type == "add_note"
  not input.action.params.text
  reason := "policy: missing text"
}

# Deny reasons: role not permitted
deny_reason[reason] {
  t := input.action.type
  not can_run_action(t)
  # only if action is recognized
  t == "resend_activation" or t == "approve_ticket" or t == "close_ticket" or t == "add_note"
  reason := sprintf("policy: role not permitted for %v", [t])
}

# Unknown action type
deny_reason[reason] {
  t := input.action.type
  not (t == "resend_activation" or t == "approve_ticket" or t == "close_ticket" or t == "add_note")
  reason := sprintf("policy: unknown action %v", [t])
}

# First deny reason helper
first_deny_reason := r {
  some rr
  deny_reason[rr]
  r := rr
}
