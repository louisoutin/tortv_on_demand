# TorTV on-demand

## Update:

They unfortunately fixed their system and they have a whitelist of mails, so this doesn't work abymore ^^

Run this to generate a m3u file to get all TV channels in HD and free for
24h.
You can then use VLC to open this m3u file (View > Playlist to change channel)

You can run it directly with:

`tortv run`                              ==> default categories

`tortv run -c "portugal english sport"`  ==> custom categories

## Install the tool

1) On ubuntu chromedriver and chrome or chromium are required:

`apt-get install chromium-chromedriver`

2) Just pip install this package locally:

`pip install .`

## Usage

Default categories ("france" and "sport"):

`tortv run `

Show the browser :

`tortv run --show` or `tortv run -s`

Use a specific channel categories:

`tortv run -l "portugal sport russ"`


Note: The available categories are in `./tortv_on_demand/categories.py`, there is not all the categories there,
you can add more by adding the checkbox value from the html page where it scraps.
