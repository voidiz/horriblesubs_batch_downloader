# horriblesubs batch downloader
a module that fetches magnet links from horriblesubs and opens them
or, alternatively, adds them to realdebrid.

## requirements
- tested on python 3.3+
- works on linux, windows, untested on macos

## installation
using setuptools (included in the python 3.4+ standard library):
```
$ python3 setup.py install
```

alternatively run the module by first installing the dependencies:
```
$ pip3 install -r requirements.txt
```
and then importing and running the module:
```
$ python3 -m horriblesubs_batch_downloader [options]
```

## usage
```
Usage:
    hsbd <url> (-a | <episode> | (<start> <end>))
               [-r <res>] [--add-to-rd]
    hsbd -n <show_name> (-a | <episode> | (<start> <end>))
               [-r <res>] [--add-to-rd]
    hsbd --set-rd-token
    hsbd -h | --help

Examples:
    # Download all episodes in the highest quality from a url:
    hsbd "https://horriblesubs.info/shows/kuzu-no-honkai" -a

    # Download episodes 1 through 5 in 720p using a show name:
    hsbd -n "Kuzu no Honkai" 1 5 -r 720

Options:
    -h, --help          Show this screen.
    -a, --all           Download all episodes.
    -n, --name          Specify show by name.
    -r, --resolution    Specify resolution (1080, 720, 480, 360).
    --add-to-rd         Add the magnet links to RealDebrid.
    --set-rd-token      Set RealDebrid API token.
```

## examples
Download all episodes in the highest quality from a url:
```
$ hsbd "https://horriblesubs.info/shows/kuzu-no-honkai" -a
```
Download episodes 1 through 5 in 720p using a show name:
```
$ hsbd -n "Kuzu no Honkai" 1 5 -r 720
```
