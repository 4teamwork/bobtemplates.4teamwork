import mrbob.cli
import sys

TARGET_DIR = 'src/'
TEMPLATE_DIR = 'ftw.bob.web:template'


def main():
    """Command Line Interface that will be available through the
    bin/create-policy script in the buildout directory.

    For now it's a simple wrapper around bin/mrbob with preconfigured
    options
    """
    args = []

    args.append('--target-directory')
    args.append(TARGET_DIR)
    args.append(TEMPLATE_DIR)

    sys.exit(mrbob.cli.main(args=args))

if __name__ == '__main__':
    main()
