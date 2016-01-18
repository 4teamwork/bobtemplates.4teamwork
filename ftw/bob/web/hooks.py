from mrbob.bobexceptions import SkipQuestion
from mrbob.bobexceptions import ValidationError
import os


def post_package_name(configurator, question, answer):
    configurator.defaults.update({
        'package.url': 'https://github.com/4teamwork/{}'.format(
            answer),
    })

    try:
        part_1, part_2 = answer.split('.')
    except ValueError:
        raise ValidationError(
            'The format of the packagename have to be e.g.: company.web')

    configurator.variables['package.part_1'] = part_1
    configurator.variables['package.part_2'] = part_2

    return answer


def pre_skip_configure_deployment(configurator, question):
    if not configurator.variables['package.configure_deployment']:
        raise(SkipQuestion)


def post_render(configurator):
    if not configurator.variables['package.configure_deployment']:
        _delete_templates_files(configurator)


def _delete_templates_files(configurator):
    import pdb; pdb.set_trace()
    package_name = configurator.variables['package.name']
    content_path = os.path.join(
        configurator.target_directory,
        'opengever.{}'.format(package_name),
        'opengever',
        package_name,
        'profiles',
        'default_content',
        'opengever_content')

    os.remove(os.path.join(content_path, '02-templates.json'))
    os.rmdir(os.path.join(content_path, 'templates'))