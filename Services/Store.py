import os
from sys import platform


def store_at_desktop(text):
    if platform == "win32":
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    else:
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

    csv_file_path = os.path.join(desktop, 'cps2.csv')

    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w') as csv_file:
            csv_file.write('{}\n'.format(text))

    else:
        with open(csv_file_path, 'a') as csv_file:
            csv_file.write('{}\n'.format(text))

