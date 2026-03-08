import typer

import subprocess
import sys
import gi
from gi.repository import Secret
from wofi import Wofi

gi.require_version('Secret', '1')

def error(msg: str):
    subprocess.run(["zenity","--error",f"--text={msg}"])

def main():
    typer.echo("Reading secrets ...")
    # Load service and all collections (metadata only, no secret values)

    try:
        service = Secret.Service.get_sync(Secret.ServiceFlags.LOAD_COLLECTIONS, None)
    except Exception as  e:
        error(f"Error loading secrets: {e}")
        raise typer.Exit(1)

    items = {}
    for collection in service.get_collections():
        collection.load_items_sync(None)
        for item in collection.get_items():
            label = item.get_label()
            items[label] = item

    if not items:
        error("no secrets found")
        raise typer.Exit(1)

    # Pick with wofi
    typer.echo("show menu via wofi")
    indices = list(items.keys())
    index, key = Wofi().select('Which secret?', indices)
    if key != 0:
        typer.echo("The user cancalled")
        raise typer.Exit(0)


    # Only fetch the secret value after selection
    label = indices[index]
    typer.echo(f"selected {label}")
    item = items.get(label)
    if not item:
        error(f"Selected item not found: {label}")
        raise typer.Exit(1)

    # Unlock the item if needed
    if item.get_locked():
        service.unlock_sync([item], None)

    try:
      item.load_secret_sync(None)
      secret = item.get_secret().get_text()
    except Exception as e:
        error(f"Error loading secret: {e}")
        raise typer.Exit(1)


    typer.echo("Typing secret", err=False)
    subprocess.run(['ydotool','type',secret], text=True)
    typer.echo("Done", err=False)

if __name__ == "__main__":
    typer.run(main)
