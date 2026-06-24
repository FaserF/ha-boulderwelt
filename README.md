# Boulderwelt Home Assistant Integration 🧗‍♂️

[![GitHub Release](https://img.shields.io/github/release/FaserF/ha-boulderwelt.svg?style=flat-square)](https://github.com/FaserF/ha-boulderwelt/releases)
[![Downloads (Current release)](https://img.shields.io/github/downloads/FaserF/ha-boulderwelt/latest/boulderwelt.zip?label=Downloads%20(Current%20release)&style=flat-square)](https://github.com/FaserF/ha-boulderwelt/releases)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/FaserF/ha-boulderwelt/ci.yml?branch=main&style=flat-square)](https://github.com/FaserF/ha-boulderwelt/actions)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![GitHub Sponsors](https://img.shields.io/badge/sponsor-GitHub-pink.svg?style=flat-square)](https://github.com/sponsors/FaserF)

Monitor the real-time occupancy of your favorite **Boulderwelt** hall directly in Home Assistant. Plan your next session when it's less crowded!

---

---

## ❤️ Support This Project

> I maintain this integration in my **free time alongside my regular job** — bug hunting, new features, and testing on real hardware. Test devices cost money, and every donation helps me stay independent and free up more time for open-source work.
>
> Donations are completely voluntary — but the more support I receive, the less I depend on other income sources and the more time I can realistically invest into these GitHub projects. 💪

<div align="center">

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor%20on-GitHub-%23EA4AAA?style=for-the-badge&logo=github-sponsors&logoColor=white)](https://github.com/sponsors/FaserF)&nbsp;&nbsp;
[![PayPal](https://img.shields.io/badge/Donate%20via-PayPal-%2300457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/FaserF)

</div>

---
## Features ✨

- **Live Occupancy**: Real-time percentage of hall utilization.
- **High Occupancy Alert**: Binary sensor indicating if the hall is currently "full" (>= 75%).
- **Multi-Location Support**: Configure multiple halls if you frequent different spots.
- **Configurable Updates**: Set your own scan interval (default: 5 minutes).
- **Native UI Configuration**: Fully supports Config Flow and Options Flow.
- **Device Support**: All entities are properly grouped under a single device per hall.

## Supported Locations 📍

- München Ost
- München Süd
- München West
- Hamburg
- Dortmund
- Frankfurt
- Karlsruhe
- Regensburg

---

## Installation 🛠️

### 1. Using HACS (Recommended)

1. Open **HACS** in your Home Assistant instance.
2. Click on **Integrations**.
3. Search for **"Boulderwelt"**.
4. Click **Download** and restart Home Assistant.

### 2. Manual Installation

1. Download the `boulderwelt.zip` from the latest [release](https://github.com/FaserF/ha-boulderwelt/releases/latest).
2. Extract the archive and copy the `custom_components/boulderwelt` directory into your Home Assistant's `custom_components` folder.
3. Restart Home Assistant.

---

## Configuration ⚙️

1. Navigate to **Settings** -> **Devices & Services**.
2. Click **Add Integration** in the bottom right.
3. Search for **"Boulderwelt"**.
4. Select your hall and set the desired update interval.

> [!TIP]
> You can change the update interval any time by clicking **Configure** on the integration card.

---

## Sensors & Entities 📊

| Entity | Type | Description |
| --- | --- | --- |
| `sensor.<hall>_occupancy` | Sensor | Current occupancy in % |
| `binary_sensor.<hall>_highly_occupied` | Binary Sensor | `on` if occupancy >= 75% (disabled by default) |

### Example Dashboard Card

```yaml
type: entities
entities:
  - entity: sensor.boulderwelt_muenchen_ost_occupancy
    name: München Ost Auslastung
  - entity: binary_sensor.boulderwelt_muenchen_ost_highly_occupied
    name: Viel los?
title: Boulderwelt 🧗
```

---

## Statistics & Daily Averages 📈

To track daily averages, you can use the built-in Home Assistant statistics platform. Add this to your `configuration.yaml`:

```yaml
sensor:
  - platform: statistics
    name: "Boulderwelt Daily Mean"
    entity_id: sensor.boulderwelt_muenchen_ost_occupancy
    state_characteristic: mean
    max_age:
      hours: 24
```

---

## Contributing 🤝

Contributions are welcome! If you find a bug or have a feature request, please open an [issue](https://github.com/FaserF/ha-boulderwelt/issues).

## Credits

- Data provided by [boulderwelt.de](https://www.boulderwelt.de/)
- Initial idea and API research by [@knorr3](https://github.com/knorr3)

---

*Disclaimer: This integration is not affiliated with, endorsed by, or supported by Boulderwelt. It uses public API endpoints provided by their website.*