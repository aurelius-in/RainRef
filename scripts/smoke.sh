#!/usr/bin/env bash
set -euo pipefail

API="${1:-http://localhost:8088}"
USER="${2:-admin@rainref.local}"
PASS="${3:-admin}"

echo "RainRef smoke against $API"

login=$(curl -sS -X POST "$API/auth/login" -H 'Content-Type: application/json' -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}")
token=$(echo "$login" | sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p')
if [ -z "$token" ]; then echo "login failed"; exit 1; fi

auth=( -H "Authorization: Bearer $token" )

evt=$(curl -sS -X POST "$API/ref/events" -H 'Content-Type: application/json' "${auth[@]}" -d '{"source":"email","channel":"support","text":"I need activation","user_ref":"u-1"}')
eid=$(echo "$evt" | sed -n 's/.*"id":"\([^"]*\)".*/\1/p')
echo "Event: $eid"

ans=$(curl -sS -X POST "$API/support/answer" -H 'Content-Type: application/json' "${auth[@]}" -d '{"source":"inbox","channel":"support","text":"I need activation","user_ref":"u-1"}')
rid=$(echo "$ans" | sed -n 's/.*"ticket_id":"\([^"]*\)".*/\1/p')
echo "Ticket: $rid"

act=$(echo "$ans" | sed -n 's/.*"actions_suggested":\(\[.*\]\).*/\1/p')
if [ "$act" != "" ] && [ "$act" != "[]" ]; then
  exec=$(curl -sS -X POST "$API/action/execute" -H 'Content-Type: application/json' "${auth[@]}" -d "$act" )
  rec=$(echo "$exec" | sed -n 's/.*"beacon_receipt_id":"\([^"]*\)".*/\1/p')
  echo "Receipt: $rec"
  curl -sS "$API/audit/$rec" "${auth[@]}" | jq . >/dev/null 2>&1 || true
fi

echo "Smoke OK"


