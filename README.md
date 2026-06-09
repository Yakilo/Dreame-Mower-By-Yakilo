# 🏡 Dreame & MOVA Lawn Mower Integration for Home Assistant

[![GitHub Release](https://img.shields.io/github/v/release/antondaubert/dreame-mower?style=flat-square)](https://github.com/antondaubert/dreame-mower/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://hacs.xyz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

A Home Assistant integration for **Dreame** and **MOVA** robotic lawn mowers. Control your mower, view maps, track mowing sessions, and monitor battery status directly from Home Assistant.

*If this integration saves you time, consider to [buy me a ☕](https://buymeacoffee.com/antondaubert).*

### Disclaimer
This is an **community-developed integration** for interoperability with Home Assistant. It is not affiliated with or supported by Dreame Technology or MOVA.

Provided "as-is" under the MIT License for personal, non-commercial use with devices you own. Use at your own risk.

## Current Features
- **Live Maps** - See your mower's location and coverage in real-time
- **Session Tracking** - Current and previous mowing sessions  
- **Session History** - Keep track of past mowing activities
- **Remote Control** - Start, pause, stop, and dock your mower
- **Map Awareness** - Inspect known maps, zones, contours, and active task metadata
- **Battery Status** - Current battery level and charging info
- **Mowing Progress** - Coverage percentage and session duration
- **Do Not Disturb** - View quiet hours settings
- **Notifications** - Status updates and error alerts

*Have suggestions? Check out [Discussions](https://github.com/antondaubert/dreame-mower/discussions)*

## UI Elements

The current release exposes map, zone, and edge selection as select entities in Home Assistant. Selecting **multiple zones or areas** at once is not yet available in the UI — use the service actions below for that.

### TODO: Hierarchical Mowing UI

The intended UI flow is:

1. Select the active map.
2. Pick a mowing scenario: all-area, edge, zone, spot, or manual.
3. If edge or zone is selected, choose one or more contours or zones.
4. If spot is selected, define the target rectangle.
5. Manual control is expected to depend on Bluetooth and remains further out in the roadmap.

The device layer already tracks map metadata and verified mowing modes so this UI can be added later without reworking the protocol layer again.

## Service Actions

Zone and area selection is available via the select entities in the UI. For mowing **multiple zones or areas** in a single run without returning to the station between them, use the service calls below.

### `dreame_mower.start_zone_mowing`

Start mowing one or more zones without the mower returning to the station between them.

```yaml
action: dreame_mower.start_zone_mowing
target:
  entity_id: lawn_mower.your_mower
data:
  zone_ids: [1, 3]
```

Zone IDs correspond to the zones defined on your map. You can find them via the zone select entities exposed by the integration.

### `dreame_mower.start_edge_mowing`

Start mowing the edges of one or more contours without the mower returning to the station between them.

```yaml
action: dreame_mower.start_edge_mowing
target:
  entity_id: lawn_mower.your_mower
data:
  contour_ids:
    - [1, 0]
    - [2, 0]
```

Contour IDs are two-integer pairs. The available pairs are exposed in the mower entity's `contours` attribute once the map has been fetched, and in the **Edge** select entity.

### `dreame_mower.start_spot_mowing`

Start mowing one or more spot areas by their IDs.

```yaml
action: dreame_mower.start_spot_mowing
target:
  entity_id: lawn_mower.your_mower
data:
  spot_area_ids: [2, 4]
```

## Installation

1. Ensure [HACS](https://hacs.xyz/) is installed
2. Navigate to HACS → Integrations
3. Click ⋮ → Custom repositories  
4. Add: `https://github.com/antondaubert/dreame-mower`
5. Category: Integration
6. Settings → Devices & Services → Add Integration → "Dreame Mower"

## Example Automations

The following is a real-world example showing how to integrate the mower with a motorized gate/cover and a rain sensor (via the [Netatmo integration](https://www.home-assistant.io/integrations/netatmo/)). Adjust entity IDs to match your setup.

### Overview

The setup consists of three parts:

1. **Mowing script** — opens the gate, waits until it is fully open, then starts the mower and sends a notification.
2. **Close-gate automation** — closes the gate automatically once the mower has docked.
3. **Daily trigger automation** — fires at noon, skips mowing if it rained today (via Netatmo), otherwise runs the mowing script.

### 1. Script: Start Mowing

This script is called by the daily trigger automation. It opens the cover/gate first and only starts the mower once the gate is confirmed open.

```yaml
alias: "[Dreame] Start Mowing"
sequence:
  - action: cover.open_cover
    target:
      entity_id: cover.dreame_gate  # replace with your cover entity
  - wait_for_trigger:
      - trigger: state
        entity_id: cover.dreame_gate
        to: "open"
    timeout: "00:01:00"
  - if:
      - condition: state
        entity_id: cover.dreame_gate
        state: "open"
    then:
      - action: lawn_mower.start_mowing
        target:
          entity_id: lawn_mower.a2  # replace with your mower entity
      - action: notify.notify
        data:
          message: "Mower started"
          title: "Dreame Mower"
```

### 2. Automation: Close Gate When Docked

Closes the gate as soon as the mower transitions from *Mowing* or *Returning* to *Docked*.

```yaml
alias: "[Dreame] Close Gate"
triggers:
  - trigger: state
    entity_id: lawn_mower.a2
    from: mowing
    to: docked
  - trigger: state
    entity_id: lawn_mower.a2
    from: returning
    to: docked
actions:
  - action: cover.close_cover
    target:
      entity_id: cover.dreame_gate
```

### 3. Automation: Daily Mowing Trigger (Rain Check)

Fires every day at noon. Uses the Netatmo integration to check whether it has rained today. If no rain is detected, the mowing script is started. Otherwise a persistent notification is sent.

```yaml
alias: "[Dreame] Daily Mowing Trigger"
triggers:
  - trigger: time
    at: "12:00:00"
actions:
  - if:
      - condition: numeric_state
        entity_id: sensor.netatmo_rainfall_today  # replace with your Netatmo rain sensor
        below: 1
    then:
      - action: script.dreame_start_mowing
    else:
      - action: notify.persistent_notification
        data:
          title: "Dreame Mower"
          message: "Mowing skipped — rain detected today."
```

> **Tip:** The daily trigger automation can be kept disabled and run on-demand via another automation or a dashboard button. The rain check prevents unnecessary mowing after wet weather.

## Community & Support

- **Discussions**: Questions and ideas → [GitHub Discussions](https://github.com/antondaubert/dreame-mower/discussions)
- **Issues**: Bug reports and feature requests → [GitHub Issues](https://github.com/antondaubert/dreame-mower/issues)

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments & Development

This integration was developed through community collaboration for the purpose of achieving interoperability with Home Assistant. It builds upon:

- [Benedikt Hübschen's](https://github.com/bhuebschen/dreame-mower) original mower integration
- Insights from [Tasshack's](https://github.com/Tasshack/dreame-vacuum) vacuum integration
- Protocol analysis and testing by the Home Assistant community

Special thanks to the entire Home Assistant community for continuous support and feedback!

---

*Happy mowing! 🌱*