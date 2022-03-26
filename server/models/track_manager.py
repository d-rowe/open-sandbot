import os
import requests
from uuid import uuid4
from datetime import datetime, timezone
import json
import time
from lib import env

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


def is_valid_track_url(url: str) -> bool:
    try:
        with requests.get(url, stream=True) as response:
            line_count = 0
            for line in response.iter_lines():
                if line_count > LINE_LIMIT:
                    return False
                if line:
                    decoded_line = line.decode('utf-8')
                    values = decoded_line.split(' ')
                    float(values[0])  # parse theta
                    rho = float(values[0])
                    if rho > 1 or rho < 0:
                        raise Exception('Rho value out of bounds')
                line_count += 1
            return True
    except:
        return False

init()
