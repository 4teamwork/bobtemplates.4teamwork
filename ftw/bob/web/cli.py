import mrbob.cli
import sys

TARGET_DIR = 'generated/'
TEMPLATE_DIR = 'ftw.bob.web:template'


def main(args=sys.argv[1:]):
    """Command Line Interface that will be available through the
    bin/create script in the buildout directory.

    For now it's a simple wrapper around bin/mrbob with preconfigured
    options
    """

    if not ('-O' in args or '--target-directory' in args):
        args.append('--target-directory')
        args.append(TARGET_DIR)

    args.append(TEMPLATE_DIR)

    sys.exit(mrbob.cli.main(args=args))

if __name__ == '__main__':
    print(main())
