# Settings File.

# Set whether this bot is running on a mobile device.
# When enabled, commands requiring local file paths (for example, /img with
# a path such as "C:\Images\Natski_Images") will be disabled.
# If you have configured your own valid paths, leave this set to False.
is_phone = False

# Time interval (in seconds) between bot ping status messages.
# Set to -1 to disable automatic ping printing.
# Recommended for debugging: <= 10 seconds.
# Default: -1
ping_delay = -1

# Enable or disable ASCII art output in the console.
# Default: True
enable_ascii = True

# Print all connected Discord guilds (server names and IDs) to the console.
# Default: True
print_guilds_connected = True

# Enable debug mode.
# This provides additional logging information and should be enabled when
# troubleshooting or reporting issues.
# Default: True
is_debugging = True

# Maximum allowed file size for uploads, in megabytes.
# Lower values reduce upload size but may decrease quality.
# Set this slightly below Discord's actual upload limit.
# Default: 9.8
file_size_limit = 9.8

# Enable Waifugame-related bot commands.
# When enabled, additional utility commands for interacting with the
# Waifugame bot will be available.
# Default: True
enable_waifugame = True