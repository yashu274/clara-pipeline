# Changelog: ACC-001
**Generated:** 2026-03-14T15:54:56.433253+00:00
**Total memo field changes:** 18
**System prompt regenerated:** Yes

---

## Memo Changes

### `after_hours_flow_summary` — *modified*
- Before: `"Clara will triage after-hours emergency dispatch, get the info, and keep trying to reach someone."`
- After:  `"Collect name, number, brief description, and tell them we'll follow up next business day. No escalation."`

### `business_hours.notes` — *modified*
- Before: `null`
- After:  `"Closed on federal holidays"`

### `business_hours.questions_or_unknowns` — *added*
- Added: `[]`

### `call_transfer_rules.max_attempts` — *modified*
- Before: `null`
- After:  `1`

### `call_transfer_rules.pre_transfer_message` — *modified*
- Before: `null`
- After:  `"I was unable to reach our on-call team directly, but I've sent them your information and they'll call you back within 15 minutes. Please keep your phone nearby."`

### `call_transfer_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `call_transfer_rules.timeout_seconds` — *modified*
- Before: `null`
- After:  `45`

### `call_transfer_rules.transfer_fail_message` — *modified*
- Before: `null`
- After:  `"I was unable to reach our on-call team directly, but I've sent them your information and they'll call you back within 15 minutes. Please keep your phone nearby."`

### `emergency_definition` — *modified*
- Before: `["active sprinkler discharge", "fire alarm activation", "flooding or actively damaging property", "smell of smoke", "fire panel fault showing a live condition"]`
- After:  `["Active sprinkler discharge", "Fire alarm signal showing a live condition on a panel", "Smoke smell reported at a site", "Flooding from a pipe failure related to our systems", "Fire panel fault showing a zone in alarm", "Carbon monoxide alarm in a building we maintain"]`

### `emergency_routing_rules` — *modified*
- Before: `[{"order": 1, "contact": "on-call dispatcher", "phone": null, "timeout_seconds": null}, {"order": 2, "contact": "lead tech", "phone": null, "timeout_seconds": null}, {"order": 3, "contact": "Diana Cho's cell", "phone": null, "timeout_seconds": null}]`
- After:  `[{"order": 1, "contact": "Dispatch line", "phone": "972-555-0148", "timeout_seconds": 45}, {"order": 2, "contact": "Brett Simmons", "phone": "972-555-0291", "timeout_seconds": 45}, {"order": 3, "contact": "Diana Cho", "phone": "972-555-0067", "timeout_seconds": 45}]`

### `integration_constraints` — *modified*
- Before: `["ServiceTrade"]`
- After:  `["Never create a sprinkler job order directly from a Clara call", "All jobs must go through our estimating team", "Extinguisher work is okay, but not sprinkler or alarm panel work", "Never quote prices"]`

### `non_emergency_routing_rules.message_to_caller` — *modified*
- Before: `null`
- After:  `"We'll follow up next business day."`

### `non_emergency_routing_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `notes` — *modified*
- Before: `null`
- After:  `"VIP accounts: Lone Star Brewery, DFW Airport Cargo (one warehouse), and Garland ISD"`

### `office_address` — *modified*
- Before: `"Garland, Texas"`
- After:  `"2847 Rowlett Road, Garland, Texas 75043"`

### `office_hours_flow_summary` — *modified*
- Before: `"Clara will handle non-emergency requests, such as inspection requests, annual certification scheduling, and quote requests."`
- After:  `"Dispatch line, then Brett's cell, then Diana's cell, then send a text to all three numbers with the caller's information and log it."`

### `questions_or_unknowns` — *modified*
- Before: `["exact phone numbers for on-call dispatcher, lead tech, and Diana Cho", "how to handle false positives", "how to handle Spanish-speaking customers"]`
- After:  `["how to handle false positives", "how to handle Spanish-speaking customers", "Clara Spanish option"]`

### `services_supported` — *modified*
- Before: `["commercial fire suppression", "sprinkler systems", "fire alarms", "suppression systems for kitchens and server rooms"]`
- After:  `["sprinkler", "extinguisher", "alarm panel"]`

## System Prompt

Prompt was **regenerated** from updated memo. See `v2/agent_spec.json` for full prompt.
