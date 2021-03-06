import sys, os, argparse, json

# Setup argparse
parser = argparse.ArgumentParser(description="This python script returns sub directories to a given directory path in an Alfred-friendly JSON object.")
parser.add_argument("-p", "--path", help="Path to the directory")
args = parser.parse_args()

project_folders = os.environ['PROJECT_FOLDER']
folders = project_folders.split(',')
if args.path:
    folders.extend(args.path)

# Script
if len(folders) > 0:
    alfredItemsObject = []

    for path in folders:
        for directory, subDirectories, subFiles in os.walk(os.path.expanduser(path)):
            for subDirectory in subDirectories:
                directoryName = subDirectory
                pathToDirectory = directory
                fullPathToSubDirectory = directory + "/" + subDirectory

                alfredItemsObject.append({
                    "uid": pathToDirectory,
                    "type": "file",
                    "title": directoryName,
                    "subtitle": fullPathToSubDirectory,
                    "arg": fullPathToSubDirectory,
                    "autocomplete": pathToDirectory,
                    "icon": {
                        "type": "fileicon",
                        "path": fullPathToSubDirectory
                    }
                })
            
            # Stop os.walk() after the first directory
            # https://stackoverflow.com/questions/43618746/os-walk-stop-looking-on-subdirectories-after-first-finding
            subDirectories[:] = []

    sys.stdout.write(json.dumps({ "items": alfredItemsObject }))
else:
    sys.stdout.write(json.dumps({ "items": [] }))
    