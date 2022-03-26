import os
import requests
from uuid import uuid4
from datetime import datetime, timezone
import json
import time
from lib import env, is_valid_track_url

if not env.is_local:
    from models import bot

track_line_limit = 5000
track_dir = 'tracks'
manifest_filename = 'manifest.json'
manifest_path = os.path.join(track_dir, manifest_filename)

in_progress = False
__force_stop = False


def stop():
    global in_progress
    global __force_stop
    if in_progress:
        __force_stop = True


def init():
    # create track folder if it doesn't yet exist
    if not os.path.isdir(track_dir):
        print('track directory does not exist, creating tracks directory')
        os.mkdir(track_dir)

    # create manifest file if it doesn't yet exist
    if not os.path.isfile(manifest_path):
        print('manifest file does not exist, creating manifest.json')
        now = __get_now()
        init_manifest = {
            'created': now,
            'tracks': []
        }
        __write_to_manifest(init_manifest)


def create_track(name: str, content: str):
    track_id = uuid4().hex
    track_path = os.path.join(track_dir, '{}.thr'.format(track_id))
    with open(track_path, 'x') as track_file:
        track_file.write(content)

    manifest_track_entry = {
        'name': name,
        'track_id': track_id,
        'created': __get_now(),
    }
    manifest = get_manifest()
    manifest['tracks'].append(manifest_track_entry)
    __write_to_manifest(manifest)
    print('New track added', manifest_track_entry)


# run track
def run(track_id: str):
    global in_progress
    global __force_stop
    in_progress = True
    track_file = '{}.thr'.format(track_id)
    track_path = os.path.join(track_dir, track_file)
    total_lines = 0
    current_line = 0

    def is_valid_line(l: str) -> bool:
        return not l.startswith('#') or l == ''

    def get_percent_complete() -> float:
        return round(current_line / total_lines * 100, 2)

    with open(track_path) as f:
        for line in f:
            # ignore comments and blank lines
            if is_valid_line(line):
                total_lines += 1

    with open(track_path) as f:
        for line in f:
            # ignore comments and blank lines
            if is_valid_line(line):
                t_r_str = line.replace('\n', '').split(' ')
                try:
                    theta = float(t_r_str[0])
                    rho = float(t_r_str[1])
                    print(theta, rho, '({}%)'.format(get_percent_complete()))
                    if env.is_local:
                        time.sleep(0.001)
                    else:
                        # handle stop command
                        if __force_stop:
                            __force_stop = False
                            break
                        bot.to_theta_rho(theta, rho)
                except ValueError:
                    print('ERROR: Cannot parse line', line)

                current_line += 1
    in_progress = False


def rename_track(track_id: str, name: str):
    manifest = get_manifest()
    for track in manifest['tracks']:
        if track.track_id == track_id:
            track.name = name
            __write_to_manifest(manifest)
            return
    raise Exception("Cannot rename track that doesn't exist: {}".format(track_id))


def import_track(url: str):
    if not is_valid_track_url(url):
        raise Exception("Invalid track file: {}".format(url))

    track_name = url.split('/')[-1]
    track_file_path = os.path.join(track_dir, track_name)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(track_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)


def get_manifest() -> dict:
    content = open(manifest_path, "r")
    return json.loads(content.read())


def __get_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def __write_to_manifest(d: dict):
    d['updated'] = __get_now()
    content = json.dumps(d, indent=4)
    with open(manifest_path, 'w') as manifest:
        manifest.write(content)


init()
