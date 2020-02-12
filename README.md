# n-hentai-scraper

![n-hentai-scraper](./logo.svg)

*"I did this for research purposes"*

## Description

This is a simple downloader for [nhentai.net](https://nhentai.net) galleries.

The downloaded galleries are currently hardcoded to store in `./data` directory.

Features:
- Just give the number and start download right away
- Download multiple doujishis at a single command!
- Downloaded images are organized by their titles
- Check, prevent & reject corrupted downloads

## Dependencies

Listed in `requirements.txt`.

## How to use

### Single gallery download

Format: `python main.py {gallery-id}`

Example: `python main.py 177013`

### Multiple gallery download at the same time (*nix OS only)

Format: `./download.sh {gallery-id}...`

Example: `./download.sh 123824 135860 141768 153521 171136 171211 186386 204241 218812 242376 297575`

## Bug Report & Suggestions

Kindly raise an issue in this repository. Not guaranteed to respond. Feel free to fork and improve.
