# horriblesubs batch downloader
a module that fetches magnet links from horriblesubs and opens them.

## requirements
- tested on python 3.3+
- works on linux, windows, untested on macos

## installation
```
python setup.py install
```

## usage
```
Usage:
    hsbd <url> (-a | <episode> | (<start> <end>)) [-r <res>]
    hsbd -n <show_name> (-a | <episode> | (<start> <end>)) [-r <res>]
    hsbd -h | --help
    
Options:
    -h, --help          Show this screen.
    -a, --all           Download all episodes.
    -n, --name          Specify show by name.
    -r, --resolution    Specify resolution (1080, 720, 480, 360).
```

## examples
```
# Download all episodes in the highest quality from a url:
hsbd "https://horriblesubs.info/shows/kuzu-no-honkai" -a

# Download episodes 1 through 5 in 720p using a show name:
hsbd -n "Kuzu no Honkai" 1 5 -r 720
```
