from collections import defaultdict
from bot.configurator import load_config

read_only = defaultdict(bool)
config = load_config('config.ini')
