# Changelog: ACC-004
**Generated:** 2026-03-14T15:55:34.482258+00:00
**Total memo field changes:** 15
**System prompt regenerated:** Yes

---

## Memo Changes

### `after_hours_flow_summary` — *modified*
- Before: `"After-hours calls are handled by on-call techs. If Pam is unavailable, go to the on-call tech."`
- After:  `"Collect name, number, company name, and brief description. Tell them we'll respond next business day. If it's Saturday during our summer hours, someone might call back same day."`

### `business_hours.questions_or_unknowns` — *added*
- Added: `[]`

### `business_hours.timezone` — *modified*
- Before: `"America/Phoenix"`
- After:  `"America/Denver"`

### `call_transfer_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `call_transfer_rules.timeout_seconds` — *modified*
- Before: `null`
- After:  `30`

### `call_transfer_rules.transfer_fail_message` — *modified*
- Before: `"Transfer failed. Please try again."`
- After:  `"I was unable to reach our on-call team directly. I've sent them your information and someone will call you within 20 minutes. Please stay near your phone."`

### `emergency_definition` — *modified*
- Before: `["Heat-related failures", "Building is uncomfortable or at risk", "Walk-in cooler down", "No cooling in August", "Office building AC out on a Monday morning", "Server room overheating"]`
- After:  `["Complete cooling failure in an occupied commercial building", "Server room overheating", "Walk-in cooler or freezer failure at a food service location", "Boiler failure in winter when the building is occupied", "Gas smell near HVAC equipment"]`

### `emergency_routing_rules` — *modified*
- Before: `[{"order": 1, "contact": "Pam (dispatch coordinator)", "phone": null, "timeout_seconds": 30}, {"order": 2, "contact": "On-call tech", "phone": null, "timeout_seconds": null}]`
- After:  `[{"order": 1, "contact": "Pam Nguyen (Dispatch Coordinator)", "phone": "480-555-0193", "timeout_seconds": 30}, {"order": 2, "contact": "On-call tech (variable)", "phone": "480-555-0276", "timeout_seconds": null}]`

### `integration_constraints` — *modified*
- Before: `["Do not create work orders in ServiceTitan. Pam handles that."]`
- After:  `["Don't create work orders from calls", "Don't promise any arrival windows", "Don't tell customers what parts cost \u2014 we quote after diagnosis"]`

### `non_emergency_routing_rules.message_to_caller` — *modified*
- Before: `"Short and professional. We'll make it efficient."`
- After:  `"We'll respond next business day. If it's Saturday during our summer hours, someone might call back same day."`

### `non_emergency_routing_rules.questions_or_unknowns` — *added*
- Added: `[]`

### `office_address` — *modified*
- Before: `"Tempe, Arizona"`
- After:  `"901 S Mill Avenue, Suite 110, Tempe, Arizona 85281"`

### `office_hours_flow_summary` — *modified*
- Before: `"During business hours, callers are routed to Pam first. If Pam doesn't answer, go to the on-call tech."`
- After:  `"Standard: Monday through Friday, 7am to 5pm Mountain time. And May 1 through September 30, we also do Saturdays 8am to noon, Mountain time."`

### `questions_or_unknowns` — *modified*
- Before: `["VIP routing rule for Pinnacle Hotels"]`
- After:  `["Pinnacle Hotels client calling numbers", "On-call tech rotation schedule"]`

### `services_supported` — *modified*
- Before: `["Commercial HVAC", "Rooftop units", "Chillers", "Boilers", "Routine maintenance", "Filter replacements", "Seasonal check-ups", "Quotes for new installs"]`
- After:  `["Commercial HVAC repair and maintenance", "Chiller and boiler service", "Rooftop unit repair", "Preventive maintenance contracts", "New commercial installs"]`

## System Prompt

Prompt was **regenerated** from updated memo. See `v2/agent_spec.json` for full prompt.
