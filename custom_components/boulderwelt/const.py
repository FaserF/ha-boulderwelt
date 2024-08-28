"""Boulderwelt"""
DOMAIN = "boulderwelt"
ATTRIBUTION = "Data provided by boulderwelt.de api"

BOULDER_HALLS = {
    "Boulderwelt München Ost",
    "Boulderwelt München Süd",
    "Boulderwelt München West",
    "Boulderwelt Hamburg",
    "Boulderwelt Dortmund",
    "Boulderwelt Frankfurt",
    "Boulderwelt Karlsruhe",
    "Boulderwelt Regensburg"
}

BOULDER_HALL_URLS = {
    "Boulderwelt München Ost": "https://www.boulderwelt-muenchen-ost.de/wp-admin/admin-ajax.php?action=cxo_get_crowd_indicator",
    "Boulderwelt München Süd": "https://www.boulderwelt-muenchen-sued.de/wp-admin/admin-ajax.php?action=cxo_get_crowd_indicator",
    "Boulderwelt München West": "https://www.boulderwelt-muenchen-west.de/wp-admin/admin-ajax.php?action=cxo_get_crowd_indicator",
    "Boulderwelt Hamburg": "https://www.boulderwelt-hamburg.de/wp-admin/admin-ajax.php?action=cxo_get_crowd_indicator",
    "Boulderwelt Dortmund": "https://www.boulderwelt-dortmund.de/wp-admin/admin-ajax.php?action=cxo_get_crowd_indicator",
    "Boulderwelt Frankfurt": "https://www.boulderwelt-frankfurt.de/wp-admin/admin-ajax.php?action=cxo_get_crowd_indicator",
    "Boulderwelt Karlsruhe": "https://www.boulderwelt-karlsruhe.de/wp-admin/admin-ajax.php?action=cxo_get_crowd_indicator",
    "Boulderwelt Regensburg": "https://www.boulderwelt-regensburg.de/wp-admin/admin-ajax.php?action=cxo_get_crowd_indicator"
}

ATTR_DATA = "data"
