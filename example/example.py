import flag
import io, sys, os

def usage(stream : io.IOBase) -> None:
    __filename__ = os.path.basename(__file__)
    __usage__    = f"Usage: {__filename__} [OPTIONS] [--] <OUTPUT FILES...>\n"
    __options__  = "OPTIONS:\n"

    stream.write(__usage__)
    stream.write(__options__)
    flag.print_options(stream)

if __name__ == "__main__":
    help  = flag.bool("help", False, "Print this help to stdout and exit with 0")
    line  = flag.str("line", "Hi!", "Line to output to the file")
    count = flag.size("count", 64, "Amount of lines to generate")

    if not flag.parse(len(sys.argv), sys.argv):
        stream = sys.stderr
        usage(stream)
        flag.print_error(stream)
        exit(1)

    if help:
        usage(sys.stdout)
        exit(0)

    rest_argc = flag.rest_argc()
    rest_argv = flag.rest_argv()

    if rest_argc <= 0:
        usage(sys.stderr)
        # with open("poop", "w") as file:
        #     usage(file)
        print("ERROR: no ouput files provided", file = sys.stderr)
        exit(1)

    for i in range(rest_argc):
        file_path = rest_argv[i]

        with open(file_path, "w") as file:
            for i in range(int(count)):
                file.write(line + "\n")

        print(f"generated {int(count)} lines in {file_path}")