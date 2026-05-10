"""Constants for the Dreame Mower integration."""

from __future__ import annotations
from typing import Final

DOMAIN = "dreame_mower"

# Configuration constants
CONF_NOTIFY: Final = "notify"
CONF_MAP_ROTATION: Final = "map_rotation"
CONF_MAP_SHOW_TITLE: Final = "map_show_title"
CONF_MAP_SHOW_LEGEND: Final = "map_show_legend"
CONF_MAP_PADDING: Final = "map_padding"

# Data storage keys
DATA_COORDINATOR = "coordinator"
DATA_PLATFORMS = "platforms"