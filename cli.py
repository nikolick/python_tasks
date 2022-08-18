import stat
from os import scandir
from datetime import datetime
from pwd import getpwuid
from grp import getgrgid
from io import StringIO
import argparse


def sort_by(entries, criterion):
    if criterion == "name":
        return sorted(entries, key=lambda e: e[0])
    elif criterion == "size":
        return sorted(entries, key=lambda e: int(e[1].st_size))
    else:
        return sorted(entries, key=lambda e: int(e[1].st_mtime))


def filter_by(entries, ftype):
    if ftype == "dir":
        return filter(lambda e: e.is_dir(), entries)
    else:
        return filter(lambda e: e.is_file(), entries)


def long_format_string(stat_info):
    file_mode_octal = str(format(stat_info.st_mode, "o"))

    dir_string = 'd' if stat.S_ISDIR(stat_info.st_mode) else '-'

    def format_permissions(octal_string):
        oct_to_string = {
            '0': '---',
            '1': '--x',
            '2': '-w-',
            '3': '-wx',
            '4': 'r--',
            '5': 'r-x',
            '6': 'rw-',
            '7': 'rwx'
        }

        return oct_to_string[octal_string[0]] \
            + oct_to_string[octal_string[1]] \
            + oct_to_string[octal_string[2]]

    permission_string = dir_string + format_permissions(file_mode_octal[-3:])
    last_modified = datetime.fromtimestamp(stat_info.st_mtime)\
        .strftime("%d/%m/%Y, %H:%M:%S")
    user = getpwuid(stat_info.st_uid).pw_name
    group = getgrgid(stat_info.st_gid).gr_name
    size = str(stat_info.st_size)
    n_links = str(stat_info.st_nlink)
    return '\t'. \
        join([permission_string, n_links, user, group, size, last_modified])


def output_to_file(fname, mode, results):
    # w - truncate
    # a - append
    # x - exclusive creation
    try:
        with open(fname, mode) as out:
            out.write(results)
    except IOError as ioe:
        # file exists and function was called with argument x
        print(ioe)
    except ValueError as ve:
        # an invalid option was passed
        print(ve)


if __name__ == '__main__':
    parser = argparse.\
        ArgumentParser(description="List contents of current folder")
    parser.add_argument('-s',
                        help="Sort entries by name/size/date modified",
                        action='store', nargs=1,
                        choices=['name', 'date', 'size'])

    parser.add_argument('-filter',
                        help="Display only subdirectories/files",
                        action='store', nargs=1, choices=['dir', 'file'])
    parser.add_argument('-l',
                        help="Detailed view of directory entries",
                        action='store_true')
    parser.add_argument('-w',
                        help="Perform file tree walk to specified depth",
                        action='store', nargs=1)
    parser.add_argument('-format',
                        help="Print entries in json/xml format",
                        action='store', nargs=1, choices=['json', 'xml'])
    parser.add_argument('-o',
                        help="Print output in specified file",
                        action='store', nargs=2)

    args = parser.parse_args()
    try:
        output = StringIO("")
        with scandir('.') as it:
            it = list(it)

            if args.filter is not None:
                it = list(filter_by(it, args.filter[0]))

            # entries_info[i][0] -> entry name
            # entries_indo[i][1] -> entry stats

            entries_info = list(zip(list(map(lambda e: e.name, it)),
                                    list(map(lambda e: e.stat(), it))))

            if args.s is not None:
                entries_info = sort_by(entries_info, args.s[0])

            for entry in entries_info:
                if args.l:
                    output.write(long_format_string(entry[1]) +
                                 '\t' + entry[0] + '\n')
                else:
                    output.write(entry[0] + '\n')

        if args.o is not None:
            output_to_file(args.o[0], args.o[1], output.getvalue())
        else:
            print(output.getvalue())
    except OSError as oe:
        print(oe)
