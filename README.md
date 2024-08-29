[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
# Boulderwelt Homeassistant Sensor
The `boulderwelt` sensor will give you informations about the current utilization of a boulderwelt hall

## Installation
### 1. Using HACS (recommended way)

This integration is a official HACS Integration.

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
- **scan interval**: Choose the time in minutes when the sensor should be refreshed

## Accessing the data

### Custom sensor
Add a custom sensor in your configuration.yaml

```yaml
- platform: template
  sensors:
    boulderwelt_location_monday_avg:
      friendly_name: "Boulderwelt location Montag Durchschnitt"
      unit_of_measurement: "%"
      value_template: >
        {% set day = now().strftime('%A') %}
        {% if day == 'Wednesday' %}
          {{ states('sensor.boulderwelt_location_level_mean') }}
        {% else %}
          {{ states('sensor.boulderwelt_location_monday_avg') }}
        {% endif %}

    boulderwelt_location_tuesday_avg:
      friendly_name: "Boulderwelt location Dienstag Durchschnitt"
      unit_of_measurement: "%"
      value_template: >
        {% set day = now().strftime('%A') %}
        {% if day == 'Thursday' %}
          {{ states('sensor.boulderwelt_location_level_mean') }}
        {% else %}
          {{ states('sensor.boulderwelt_location_tuesday_avg') }}
        {% endif %}

    boulderwelt_location_wednesday_avg:
      friendly_name: "Boulderwelt location Mittwoch Durchschnitt"
      unit_of_measurement: "%"
      value_template: >
        {% set day = now().strftime('%A') %}
        {% if day == 'Wednesday' %}
          {{ states('sensor.boulderwelt_location_level_mean') }}
        {% else %}
          {{ states('sensor.boulderwelt_location_wednesday_avg') }}
        {% endif %}

    boulderwelt_location_thursday_avg:
      friendly_name: "Boulderwelt location Donnerstag Durchschnitt"
      unit_of_measurement: "%"
      value_template: >
        {% set day = now().strftime('%A') %}
        {% if day == 'Thursday' %}
          {{ states('sensor.boulderwelt_location_level_mean') }}
        {% else %}
          {{ states('sensor.boulderwelt_location_thursday_avg') }}
        {% endif %}

    boulderwelt_location_friday_avg:
      friendly_name: "Boulderwelt location Freitag Durchschnitt"
      unit_of_measurement: "%"
      value_template: >
        {% set day = now().strftime('%A') %}
        {% if day == 'Thursday' %}
          {{ states('sensor.boulderwelt_location_level_mean') }}
        {% else %}
          {{ states('sensor.boulderwelt_location_friday_avg') }}
        {% endif %}

- platform: statistics
  name: "Boulderwelt Location Level Mean"
  entity_id: sensor.boulderwelt_location_level
  state_characteristic: mean
  max_age:
    hours: 24
  sampling_size: 24
```

### Automations
```yaml
automation:
  - id: update_boulderwelt_sensor_average
    alias: "Update Boulderwelt Sensor Average"
    trigger:
      - platform: time
        at: "23:59:00"
    action:
      - choose:
          - conditions:
              - condition: time
                weekday:
                  - mon
            sequence:
              - service: homeassistant.update_entity
                target:
                  entity_id:
                    - sensor.boulderwelt_location_monday_avg

          - conditions:
              - condition: time
                weekday:
                  - tue
            sequence:
              - service: homeassistant.update_entity
                target:
                  entity_id:
                    - sensor.boulderwelt_location_tuesday_avg

          - conditions:
              - condition: time
                weekday:
                  - wed
            sequence:
              - service: homeassistant.update_entity
                target:
                  entity_id:
                    - sensor.boulderwelt_location_wednesday_avg

          - conditions:
              - condition: time
                weekday:
                  - thu
            sequence:
              - service: homeassistant.update_entity
                target:
                  entity_id:
                    - sensor.boulderwelt_location_thursday_avg

          - conditions:
              - condition: time
                weekday:
                  - fri
            sequence:
              - service: homeassistant.update_entity
                target:
                  entity_id:
                    - sensor.boulderwelt_location_friday_avg

          - conditions:
              - condition: time
                weekday:
                  - sat
            sequence:
              - service: homeassistant.update_entity
                target:
                  entity_id:
                    - sensor.boulderwelt_location_saturday_avg

          - conditions:
              - condition: time
                weekday:
                  - sun
            sequence:
              - service: homeassistant.update_entity
                target:
                  entity_id:
                    - sensor.boulderwelt_location_sunday_avg
```

```yaml
automation:
  - id: remind_for_bouldern
    alias: "remind for Bouldern"
    trigger:
      - platform: time
        at: "19:00:00"
    condition:
      - condition: time
        weekday:
          - sun
    action:
      - service: telegram_bot.send_message
        data:
          target: !secret telegram_chat_bouldern
          message: >
            {% set days_location = [
              {'day': 'Montag', 'value': states('sensor.boulderwelt_location_monday_avg') | float(70)},
              {'day': 'Dienstag', 'value': states('sensor.boulderwelt_location_tuesday_avg') | float(70)},
              {'day': 'Mittwoch', 'value': states('sensor.boulderwelt_location_wednesday_avg') | float(70)},
              {'day': 'Donnerstag', 'value': states('sensor.boulderwelt_location_thursday_avg') | float(70)},
              {'day': 'Freitag', 'value': states('sensor.boulderwelt_location_friday_avg') | float(70)}
            ] %}
            {% set sorted_days_location = days_location | sort(attribute='value') %}
            The best days to go to the hall in the weekdays, based on the utilization from last week are: 
            1. {{ sorted_days_location[0].day }} (Durchschnittliche Auslastung: {{ sorted_days_location[0].value }} %)
            2. {{ sorted_days_location[1].day }} (Durchschnittliche Auslastung: {{ sorted_days_location[1].value }} %)
            3. {{ sorted_days_location[2].day }} (Durchschnittliche Auslastung: {{ sorted_days_location[2].value }} %)

            {% set days_weekend_location = [
              {'day': 'Samstag', 'value': states('sensor.boulderwelt_location_saturday_avg') | float(70)},
              {'day': 'Sonntag', 'value': states('sensor.boulderwelt_location_sunday_avg') | float(70)}
            ] %}
            {% set sorted_days_weekend_location = days_weekend_location | sort(attribute='value') %}
            The best day at the weekend to go to the hall, based on the utilization from last week is: 
            {{ sorted_days_weekend_location[0].day }} (Durchschnittliche Auslastung: {{ sorted_days_weekend_location[0].value }} %)
```

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