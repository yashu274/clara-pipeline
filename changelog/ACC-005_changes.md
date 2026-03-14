# Changelog: ACC-005
**Generated:** 2026-03-14T15:55:49.398201+00:00
**Total memo field changes:** 9
**System prompt regenerated:** Yes

---

## Memo Changes

### `after_hours_flow_summary` — *modified*
- Before: `"Collect caller's information and tell them we'll call back next business day."`
- After:  `"For after-hours: true emergency is extinguisher failure in a fire, or post-discharge suppression inspection. Everything else is next business day."`

### `business_hours.questions_or_unknowns` — *added*
- Added: `[]`

### `call_transfer_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `emergency_definition` — *modified*
- Before: `["extinguisher failure during a fire event", "condemned suppression system"]`
- After:  `["Fire extinguisher that failed to operate during an actual fire event", "Kitchen suppression system that discharged and needs immediate inspection before the restaurant can reopen"]`

### `emergency_routing_rules` — *modified*
- Before: `[{"order": 1, "contact": "911", "phone": "911", "timeout_seconds": null}]`
- After:  `[{"order": 1, "contact": "Raymond Torres", "phone": "713-555-0182", "timeout_seconds": 30}]`

### `integration_constraints` — *modified*
- Before: `["do not create anything in Wintac", "do not promise anything to customers about upcoming inspections"]`
- After:  `["Never create anything in Wintac from a call", "Never quote prices", "Don't promise inspection dates"]`

### `non_emergency_routing_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `office_address` — *modified*
- Before: `"Houston, Texas, in the Heights neighborhood"`
- After:  `"1402 Heights Boulevard, Houston, Texas 77008"`

### `services_supported` — *modified*
- Before: `["fire extinguisher sales", "service", "certification", "exit and emergency lighting inspection"]`
- After:  `["Fire extinguisher sales", "Fire extinguisher service", "Annual certification", "Emergency lighting inspection", "Exit sign inspection", "Kitchen hood suppression system inspection", "Fire safety training"]`

## System Prompt

Prompt was **regenerated** from updated memo. See `v2/agent_spec.json` for full prompt.
