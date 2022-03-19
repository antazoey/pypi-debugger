import click
import pypistats
import json
from subprocess import check_output
import requests
import dateutil.parser as dp
import datetime


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name")
def stats(name):
    click.echo(pypistats.recent(name))


@cli.command()
@click.option("--days-ago", default=7, help="Check for releases in the past X days.")
def new_releases(days_ago):
    dep_tree_output = check_output(["pipdeptree", "--json"])
    dependencies = json.loads(dep_tree_output)

    now = datetime.datetime.utcnow()
    timestamp = (now - datetime.timedelta(days=days_ago)).timestamp()

    for dep in dependencies:
        name = dep["package"]["package_name"]
        base_url = f"https://pypi.org/pypi/{name}/json"
        response = requests.get(base_url)

        if response.status_code == 404:
            # Non-published package
            continue

        response.raise_for_status()
        releases = response.json()["releases"]

        if not len(releases):
            continue

        # NOTE: Assuming greatest release is always at the end
        greatest_version = [k for k in releases.keys()][-1]
        latest_releases = releases[greatest_version]
        for release in latest_releases:
            release_time = release["upload_time_iso_8601"]
            parsed_release_time = dp.parse(release_time).timestamp()
            if parsed_release_time >= timestamp:
                click.echo(f"{name} was released on {release_time}")
