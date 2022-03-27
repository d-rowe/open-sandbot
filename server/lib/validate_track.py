import requests

LINE_LIMIT = 5000


def validate_track(url: str) -> bool:
    with requests.get(url, stream=True) as response:
        line_count = 0
        for line in response.iter_lines():
            if line_count > LINE_LIMIT:
                raise ValueError('File exceeds max line count of {}'.format(LINE_LIMIT))
            if line:
                decoded_line = line.decode('utf-8')
                values = decoded_line.split(' ')
                float(values[0])  # parse theta
                rho = float(values[1])
                if rho > 1 or rho < 0:
                    raise ValueError('Rho value out of bounds')
            line_count += 1
