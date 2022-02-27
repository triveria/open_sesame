"""Console script for open_sesame."""
import sys
import click
# from open_sesame import open_sesame
import open_sesame


@click.group(context_settings=dict(max_content_width=999))
# @click.version_option(version=open_sesame.__version__)
def main():
    """
    Add description about program here.
    """
    pass


@main.command()
@click.option("--cfg") #, type=click.Path, help="")
def run(cfg):
    open_sesame.run(cfg)
    return 0


@main.command()
def add():
    print("adding")
    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
