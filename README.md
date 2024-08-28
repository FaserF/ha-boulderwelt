[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
# Boulderwelt Homeassistant Sensor
The `boulderwelt` sensor will give you informations about the current utilization of a boulderwelt hall

## Installation
### 1. Using HACS (recommended way)

This integration is soon a official HACS Integration.

Open HACS then install the "Boulderwelt" integration or use the link below.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=FaserF&repository=ha-boulderwelt&category=integration)

If you use this method, your component will always update to the latest version.

### 2. Manual

- Download the latest zip release from [here](https://github.com/FaserF/ha-boulderwelt/releases/latest)
- Extract the zip file
- Copy the folder "boulderwelt" from within custom_components with all of its components to `<config>/custom_components/`

where `<config>` is your Home Assistant configuration directory.

>__NOTE__: Do not download the file by using the link above directly, the status in the "master" branch can be in development and therefore is maybe not working.

## Configuration

Go to Configuration -> Integrations and click on "add integration". Then search for "Boulderwelt".

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=boulderwelt)

### Configuration Variables
- **boulder hall**: Select the boulderwelt boulder hall, from where the data should be fetched

## Bug reporting
Open an issue over at [github issues](https://github.com/FaserF/ha-boulderwelt/issues). Please prefer sending over a log with debugging enabled.

To enable debugging enter the following in your configuration.yaml

```yaml
logger:
    logs:
        custom_components.boulderwelt: debug
```

You can then find the log in the HA settings -> System -> Logs -> Enter "boulderwelt" in the search bar -> "Load full logs"

## Thanks to
Huge thanks to [@knorr3](https://github.com/knorr3) for finding the json files from boulderwelt and the idea!

The data is coming from the corresponding [boulderwelt.de](https://www.boulderwelt.de/) website.