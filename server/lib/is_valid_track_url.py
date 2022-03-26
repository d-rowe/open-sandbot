import requests

LINE_LIMIT = 5000


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
