import bot


def run(track: str):
    track_file = '{}.thr'.format(track)
    total_lines = 0
    current_line = 0

    def is_valid_line(l: str) -> bool:
        return not l.startswith('#') or l == ''

    def get_percent_complete() -> float:
        return round(current_line / total_lines * 100, 2)

    with open(track_file) as f:
        for line in f:
            # ignore comments and blank lines
            if is_valid_line(line):
                total_lines += 1

    with open(track_file) as f:
        for line in f:
            # ignore comments and blank lines
            if is_valid_line(line):
                t_r_str = line.replace('\n', '').split(' ')
                try:
                    theta = float(t_r_str[0])
                    rho = float(t_r_str[1])
                    print(theta, rho, '({}%)'.format(get_percent_complete()))
                    bot.to_theta_rho(theta, rho)
                except ValueError:
                    print('ERROR: Cannot parse line', line)

                current_line += 1

    print('Finished')
    print('Homing and exiting')
    bot.exit()
