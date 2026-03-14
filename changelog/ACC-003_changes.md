# Changelog: ACC-003
**Generated:** 2026-03-14T15:55:20.434749+00:00
**Total memo field changes:** 12
**System prompt regenerated:** Yes

---

## Memo Changes

### `business_hours.questions_or_unknowns` — *added*
- Added: `[]`

### `call_transfer_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `call_transfer_rules.timeout_seconds` — *modified*
- Before: `null`
- After:  `40`

### `call_transfer_rules.transfer_fail_message` — *modified*
- Before: `null`
- After:  `"I was unable to reach our on-call team right now. I have your information and our operations team has been notified by alert. Someone will contact you within 20 minutes."`

### `emergency_definition` — *modified*
- Before: `["live alarm situation", "break-ins", "sensor malfunctioned"]`
- After:  `["Live alarm signal from a monitored account", "Customer reports break-in in progress or has confirmed a fire", "Malfunctioning system causing false alarms", "Customer's panel is offline and their building is unprotected"]`

### `emergency_routing_rules` — *modified*
- Before: `[{"order": 1, "contact": "on-call tech", "phone": null, "timeout_seconds": null}, {"order": 2, "contact": "monitoring coordinator", "phone": null, "timeout_seconds": null}]`
- After:  `[{"order": 1, "contact": "Priya, monitoring coordinator", "phone": "404-555-0217", "timeout_seconds": 40}, {"order": 2, "contact": "Mike, Lead Technician", "phone": "404-555-0382", "timeout_seconds": 40}, {"order": 3, "contact": "James, backup coordinator", "phone": "404-555-0459", "timeout_seconds": null}]`

### `integration_constraints` — *modified*
- Before: `["no direct ticket creation in Alarm.com or ServiceMax"]`
- After:  `["Clara must never promise to create a ticket in ServiceMax", "Never confirm monitoring status over the phone", "Never give out technician cell numbers to customers"]`

### `non_emergency_routing_rules.collect_fields` — *modified*
- Before: `["name", "phone", "description"]`
- After:  `["name", "phone", "account number", "description"]`

### `non_emergency_routing_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `office_address` — *modified*
- Before: `"Buckhead, Atlanta"`
- After:  `"3100 Piedmont Road NE, Suite 200, Atlanta, Georgia 30305"`

### `questions_or_unknowns` — *modified*
- Before: `["timeout_seconds for emergency_routing_rules", "phone numbers for emergency_routing_rules"]`
- After:  `[]`

### `services_supported` — *modified*
- Before: `["fire and burglar alarms"]`
- After:  `["Fire alarm installation and monitoring", "Burglar alarm installation and monitoring", "Access control", "CCTV", "Annual inspections"]`

## System Prompt

Prompt was **regenerated** from updated memo. See `v2/agent_spec.json` for full prompt.
