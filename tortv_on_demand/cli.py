import sys
from docopt import docopt
import tortv_on_demand
from tortv_on_demand.main import process


def run_main():
    """
    Mixture Density Networks

    Usage:
      tortv run -s | --show
      tortv run
      tortv -h | --help
      tortv --version

    Options:
      -h --help     Show this screen.
      -s --show     Show the
      --version     Show version.
    """

    if len(sys.argv) == 0:
        sys.argv.append("--help")
    arguments = docopt(
        run_main.__doc__,
        version="tortv v.%s - tortv on demand" % tortv_on_demand.version,
    )
    print(arguments)
    if arguments["run"]:
        show = False
        if arguments["--show"]:
            show = True
        process(show)


if __name__ == "__main__":
    run_main()
