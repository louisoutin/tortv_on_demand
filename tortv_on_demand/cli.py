import sys
from docopt import docopt
import tortv_on_demand
from tortv_on_demand.main import process


def run_main():
    """
    TorTV On Demand.
    Run this to generate a m3u file to get all TV channels in HD and free for
    24h.

    You can run it directly with:

    `tortv run`                              ==> default categories
    `tortv run -c "portugal english sport"`  ==> custom categories

    Availables categories for now:
        - "english"
        - "portugal"
        - "france"
        - "sport"
        - "spanish"
        - "russ"

    Usage:
      tortv run [-s | --show]
      tortv run [-c | --categories] <categories> [-s | --show]
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
    if arguments["run"]:
        show = False
        if arguments["--show"]:
            show = True
        if arguments["<categories>"] is not None:
            categories = arguments["<categories>"].split()
        else:
            categories = ["france", "sport"]
        process(show, categories)


if __name__ == "__main__":
    run_main()
