from argparse import ArgumentParser

from bot import runner
from bot.configurator import load_config


def main():
    """

    :return:
    """
    parser = ArgumentParser()
    parser.add_argument("--config", type=str)

    args = parser.parse_args()

    config = load_config(args.config)

    runner.run(config)

main()
