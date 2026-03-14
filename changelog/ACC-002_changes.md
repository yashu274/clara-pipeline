# Changelog: ACC-002
**Generated:** 2026-03-14T15:55:07.366853+00:00
**Total memo field changes:** 16
**System prompt regenerated:** Yes

---

## Memo Changes

### `after_hours_flow_summary` — *modified*
- Before: `"Clara will try to reach Kevin and then Dave during after-hours."`
- After:  `"Collect name, callback number, and one sentence about the issue. Tell them I'll call back next business day."`

### `business_hours.questions_or_unknowns` — *added*
- Added: `[]`

### `call_transfer_rules.pre_transfer_message` — *modified*
- Before: `null`
- After:  `"We'll have someone contact you shortly."`

### `call_transfer_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `call_transfer_rules.timeout_seconds` — *modified*
- Before: `null`
- After:  `30`

### `call_transfer_rules.transfer_fail_message` — *modified*
- Before: `null`
- After:  `"I was unable to reach a technician directly. I've left an urgent message and Kevin will call you back within 30 minutes. Please stay available."`

### `emergency_definition` — *modified*
- Before: `["active water flow from a sprinkler head", "visible flooding in a mechanical room", "accidental head hit", "fire panel alerts from a building that's currently occupied"]`
- After:  `["Active water discharge from a sprinkler head", "Accidental head activation", "Flooding inside a building from a pipe failure"]`

### `emergency_routing_rules` — *modified*
- Before: `[{"order": 1, "contact": "Kevin Okafor", "phone": "312 area code (number not specified)", "timeout_seconds": null}, {"order": 2, "contact": "Dave (Kevin's tech)", "phone": "312 area code (number not specified)", "timeout_seconds": null}]`
- After:  `[{"order": 1, "contact": "Kevin Okafor", "phone": "312-555-0182", "timeout_seconds": 30}, {"order": 2, "contact": "Dave", "phone": "312-555-0349", "timeout_seconds": 30}]`

### `integration_constraints` — *modified*
- Before: `["Google Sheets"]`
- After:  `["Don't promise arrival times"]`

### `non_emergency_routing_rules.message_to_caller` — *modified*
- Before: `null`
- After:  `"I'll call back next business day."`

### `non_emergency_routing_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `notes` — *modified*
- Before: `null`
- After:  `"Keep it simple."`

### `office_address` — *modified*
- Before: `"Naperville, Illinois"`
- After:  `"412 Ogden Avenue, Naperville, Illinois 60563"`

### `office_hours_flow_summary` — *modified*
- Before: `"Clara will try to reach Kevin and then Dave during business hours."`
- After:  `"Try my cell first \u2014 312-555-0182. If I don't answer in 30 seconds, try Dave at 312-555-0349. If Dave doesn't answer in 30 seconds, leave a voicemail on my cell and tell the caller I'll call back within 30 minutes."`

### `questions_or_unknowns` — *modified*
- Before: `["exact escalation path", "Dave's phone number"]`
- After:  `["Special accounts", "exact escalation path"]`

### `services_supported` — *modified*
- Before: `["sprinkler installation", "sprinkler repair", "inspection scheduling", "quote requests"]`
- After:  `["Sprinkler installation", "Sprinkler repair", "Sprinkler service", "Backflow preventer testing", "Annual inspections"]`

## System Prompt

Prompt was **regenerated** from updated memo. See `v2/agent_spec.json` for full prompt.
