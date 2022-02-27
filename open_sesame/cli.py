"""Console script for open_sesame."""
import sys
import click
from open_sesame import open_sesame


@click.command()
def main(args=None):
    open_sesame.main("")
    return 0



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
