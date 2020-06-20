# %****G_Code_Reverser****%#


import re
import argparse
from pathlib import Path

inizio_estrusione = '''

hull_polyline3d (

    points = [
'''

fine_estrusione = '''
surgit
    ]
);

'''


def _filter_gcode_lines(gcode_lines):
    """
    Clean useless lines from gcode
    """

    letters = ['a', 'b', 'c', 'd',
               'h', 'i', 'l', 'm',
               'n', 'o', 'p', 'q',
               'r', 's', 't', 'u',
               'v']

    patterns = ['F[0-9. ]+',
                'E[0-9.\- ]+',
                'G1']

    cleaned_lines = []

    for k in gcode_lines:

        condition1 = (k.startswith('G1') | k.startswith('G0'))
        condition2 = (not any(letter in k for letter in letters))

        if condition1 & condition2:

            for p in patterns:
                k = re.sub(p, '', k)

            if 'Z' in k:
                k = re.sub('X[0-9.\- ]+', '', k)
                k = re.sub('Y[0-9.\- ]+', '', k)

            if 'G0' in k:
                k = re.sub('G0', '', k)

            cleaned_lines.append(k)

    return cleaned_lines


def _convert_gcode_cleaned(cleaned_lines):

    list_to_file = []

    z_value = None

    first_row_blocco = True

    for index, q in enumerate(cleaned_lines):

        if "Z" in q:

            z_value = str(q.replace('Z', '')).strip()

            first_row_blocco = True

        if "X" in q:

            if first_row_blocco:

                list_to_file.append(inizio_estrusione)

                first_row_blocco = False

            string_split = q.split(" ")

            x_value = str(string_split[1].replace('X', ''))

            y_value = str(string_split[2].replace('Y', ''))

            new_string = '[' + x_value + ',' + y_value + ',' + z_value + '],'

            list_to_file.append(new_string)

            if len(cleaned_lines[index + 1].strip()) == 0:

                list_to_file.append(fine_estrusione)

    return list_to_file


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Gcode file to convert')
    parser.add_argument('-o', '--output', help="Output filename")

    args = parser.parse_args()

    gcode_path = Path(args.input).absolute()

    template = Path(__file__).parent.absolute() / 'template.scad'

    if args.output is None:
        output = Path(str(gcode_path.name).replace(
            '.gcode', '.scad')).absolute()
    else:
        output = Path(args.output).absolute()

    print(f'Converting {gcode_path} to {output}')
    gcode_lines = gcode_path.read_text().splitlines()

    cleaned_lines = _filter_gcode_lines(gcode_lines)

    list_to_file = _convert_gcode_cleaned(cleaned_lines)

    output_text = [template.read_text()] + list_to_file
    output_text = "\n".join(output_text)

    output.write_text(output_text)


if __name__ == '__main__':

    main()
