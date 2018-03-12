from mrbob.cli import parser
from mrbob.parsing import parse_config
import logging
import mrbob.cli
import os
import shutil
import subprocess
import sys
import tox

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bobtemplates.4teamwork')

# This templates are allowed to create.
# Key: Template-Name
# Value: 'mr.bob template-path'
AVAILABLE_TEMPLATES = {
    'django': 'bobtemplates:django',
    'web': 'bobtemplates:web',
    'intranet': 'bobtemplates:intranet',
    'workspace': 'bobtemplates:workspace',
    'module': 'bobtemplates:module',
    'javascript': 'bobtemplates:javascript',
    }

# example: ~/projects/bobtemplates.4teamwork
MODULE_PATH = os.path.dirname(__file__)

# example: ~/projects/bobtemplates.4teamwork/bobtemplates
TEMPLATES_PATH = os.path.join(MODULE_PATH, 'bobtemplates')

# example: ~/projects/bobtemplates.4teamwork/scripts
SCRIPTS_PATH = os.path.join(MODULE_PATH, 'scripts')

# example: ~/projects/bobtemplates.4teamwork/autogenerate
AUTOGENERATE_CONFIG_PATH = os.path.join(MODULE_PATH, 'autogenerate')

# Generated packages will be stored in this folder
TARGET_DIR = os.path.join(MODULE_PATH, 'generated')


class FSFolderContext(object):
    """ Contextmanager: Changes the current
    FS directory to the given path.
    """
    def __init__(self, path):
        self._old_path = os.getcwd()
        self._path = path

    def __enter__(self):
        os.chdir(self._path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self._old_path)


class BobConfig(object):

    config = None

    def __init__(self, config_path):
        self.config = parse_config(config_path)

    def get(self, name):
        value = self.config['variables'].get(name)

        if value and isinstance(value, unicode):
            value = value.encode('utf-8')

        return value


class Converter(object):

    config = None

    def __init__(self, bob_config):
        self.config = bob_config

    def convert(self, path, excluded_filenames=[]):

        for folder_path, subfolder_names, file_names in os.walk(path, topdown=False):
            for file_name in file_names:
                if file_name in excluded_filenames:
                    continue

                file_path = os.path.join(folder_path, file_name)

                self.convert_file_content(file_path)
                self.rename_fs_obj_name(file_path)

            self.rename_fs_obj_name(folder_path)

    def convert_file_content(self, path):
        with open(path, 'r+') as file_:
            data = self.replace_content(file_.read())
            file_.seek(0)
            file_.write(data)
            file_.truncate()

    def rename_fs_obj_name(self, path):
        folder_name = os.path.dirname(path)
        obj_name = os.path.basename(path)

        if os.path.isfile(path):
            obj_name = '{}.bob'.format(obj_name)

        obj_name = self.replace_path(obj_name)
        os.rename(path, os.path.join(folder_name, obj_name))

    def replace_path(self, text):
        text = text.replace(
            self.config.get('package.fullname'),
            '+package.fullname+')

        text = text.replace(
            self.config.get('package.fullname_underscore'),
            '+package.fullname_underscore+')

        text = text.replace(
            self.config.get('package.part_1'),
            '+package.part_1+')

        text = text.replace(
            self.config.get('package.part_2'),
            '+package.part_2+')

        return text

    def replace_content(self, text):
        """Replaces known strings with the mr.bob variables.
        """
        text = text.replace(
            self.config.get('package.fullname'),
            '{{{package.fullname}}}')

        text = text.replace(
            self.config.get('package.fullname_underscore'),
            '{{{package.fullname_underscore}}}')

        text = text.replace(
            self.config.get('package.part_1'),
            '{{{package.part_1}}}')

        text = text.replace(
            self.config.get('package.part_2'),
            '{{{package.part_2}}}')

        return text


class TemplateGeneratorCLI(object):

    args = None
    options = None
    template_name = None
    config = None

    template_config_path = None

    generated_package_path = None

    template_workflow_dir_path = None
    generated_workflow_dir_path = None

    template_locales_dir_path = None
    generated_locales_dir_path = None

    def __init__(self, args):
        self.args = args
        self.options = parser.parse_args(args=self.args)
        self.template_name = self.options.template

        self.validate_template_name()

        self._set_default_template_for_args()
        self._extend_args_with_target_directory()

        self.template_config_path = os.path.join(
            AUTOGENERATE_CONFIG_PATH, '{}.ini'.format(self.template_name))

        self.config = BobConfig(self.template_config_path)

        self.generated_package_path = os.path.join(
            MODULE_PATH, TARGET_DIR, self.config.get('package.fullname'))

        self.template_workflow_dir_path = os.path.join(
            TEMPLATES_PATH,
            self.template_name,
            '+package.fullname+/+package.part_1+/+package.part_2+/'
            'profiles/default/workflows')

        self.generated_workflow_dir_path = os.path.join(
            self.generated_package_path,
            self.config.get('package.part_1'),
            self.config.get('package.part_2'),
            'profiles/default/workflows')

        self.template_locales_dir_path = os.path.join(
            TEMPLATES_PATH,
            self.template_name,
            '+package.fullname+/+package.part_1+/+package.part_2+/locales')

        self.generated_locales_dir_path = os.path.join(
            self.generated_package_path,
            self.config.get('package.part_1'),
            self.config.get('package.part_2'),
            'locales',
            )

    def generate_package(self, args=None):
        args = args or self.args
        mrbob.cli.main(args=args)

    def autogenerate_package(self):
        self._remove_fs_object_by_path(self.generated_package_path)

        autogenerate_args = self.args
        autogenerate_args.append('--non-interactive')
        autogenerate_args.extend(['--config', self.template_config_path])

        self.generate_package(args=autogenerate_args)

    def buildout(self):
        with FSFolderContext(self.generated_package_path):
            logger.info(
                "Run buildout for package {}".format(os.getcwd()))

            os.symlink('development.cfg', 'buildout.cfg')

            subprocess.check_call([sys.executable, 'bootstrap.py'])
            subprocess.check_call(['bin/buildout'])

    def run_template_tests(self):
        with FSFolderContext(self.generated_package_path):
            logger.info(
                "Run tests for package {}".format(os.getcwd()))

            subprocess.check_call(['bin/test'])

    def setup_plone_site(self):
        with FSFolderContext(self.generated_package_path):
            logger.info(
                "Setup plonesite for package {}".format(os.getcwd()))

            subprocess.check_call([
                'bin/instance',
                'run',
                os.path.join(SCRIPTS_PATH, 'setup_plone_site.py')])

    def update_workflow(self):
        with FSFolderContext(self.generated_package_path):
            logger.info(
                "Update workflow for package {}".format(os.getcwd()))

            subprocess.check_call(['bin/instance', 'rebuild_workflows --site platform'])

    def write_back_workflow(self):
        logger.info(
            "Write back workflow for package {}".format(self.generated_package_path))

        # Remove old workflow definition from template
        self._remove_fs_object_by_path(self.template_workflow_dir_path)

        # Copy generated workflow definition into the template directory
        shutil.copytree(
            self.generated_workflow_dir_path,
            self.template_workflow_dir_path)

        converter = Converter(self.config)
        converter.convert(
            self.template_workflow_dir_path,
            excluded_filenames=['.gitignore', 'result.xml.bob'])

    def write_back_translations(self):
        logger.info(
            "Write back translations for package {}".format(self.generated_package_path))

        # Remove old workflow definition from template
        self._remove_fs_object_by_path(self.template_locales_dir_path)

        # Copy generated translations into the template directory
        shutil.copytree(
            self.generated_locales_dir_path,
            self.template_locales_dir_path)

        self.remove_files_recursive(self.template_locales_dir_path, '.mo')

        converter = Converter(self.config)
        converter.convert(self.template_locales_dir_path)

    def validate_template_name(self):
        if self.template_name and self.template_name in AVAILABLE_TEMPLATES.keys():
            return True

        logger.error(
            "\n" +
            "Please specify a template: bin/create template-name\n"
            "---------------------------------------------------\n"
            "Available templates:\n\n"
            "{templates}\n".format(
                templates='\n'.join(AVAILABLE_TEMPLATES.keys()))
            )

        sys.exit()

    def remove_files_recursive(self, path, extension=""):
        for subdir, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(subdir, file)

                filename, file_extension = os.path.splitext(file_path)

                if not file_extension == extension:
                    continue

                self._remove_fs_object_by_path(file_path)
                continue

    def _remove_fs_object_by_path(self, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    def _extend_args_with_target_directory(self):
        if not ('-O' in self.args or '--target-directory' in self.args):
            self.args.append('--target-directory')
            self.args.append(TARGET_DIR)

    def _set_default_template_for_args(self):
        self.args[0] = AVAILABLE_TEMPLATES.get(self.template_name)


def main(args=sys.argv[1:]):
    """Command Line Interface that will be available through the
    bin/create script in the buildout directory.

    For now it's a simple wrapper around bin/mrbob with preconfigured
    options
    """
    generator = TemplateGeneratorCLI(args)

    generator.generate_package()


def autogenerate(args=sys.argv[1:]):
    """Command Line Interface that will autogenerate the given template.
    """
    generator = TemplateGeneratorCLI(args)

    generator.autogenerate_package()


def template_test(args=sys.argv[1:]):
    """Command Line Interface that will test the autogenerated package.
    """
    generator = TemplateGeneratorCLI(args)

    generator.autogenerate_package()
    generator.buildout()
    generator.run_template_tests()


def buildout_template(args=sys.argv[1:]):
    """Command Line Interface that will buildout the autogenerated package.
    """
    generator = TemplateGeneratorCLI(args)

    generator.autogenerate_package()
    generator.buildout()


def update_lawgiver_workflow(args=sys.argv[1:]):
    """Command Line Interface that will update the lawgiver workflow.
    """
    generator = TemplateGeneratorCLI(args)

    generator.autogenerate_package()
    generator.buildout()
    generator.setup_plone_site()
    generator.update_workflow()

    generator.write_back_workflow()
    generator.write_back_translations()


def fulltest(args=sys.argv[1:]):
    """Command Line Interface that will update the lawgiver-workflow
    and test the package.
    """
    generator = TemplateGeneratorCLI(args)

    generator.autogenerate_package()
    generator.buildout()
    generator.setup_plone_site()
    generator.update_workflow()

    generator.write_back_workflow()
    generator.write_back_translations()

    generator.autogenerate_package()
    generator.buildout()
    generator.run_template_tests()
