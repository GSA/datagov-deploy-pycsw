import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

app_user = 'pycsw'
python_version = '3.6.12'
deployment_version = '20190308132800Z'


# python major minor version e.g. 3.6
python_major_minor_version = '.'.join(python_version.split('.')[:2])


def test_app_home(host):
    home = host.file('/home/%s' % app_user)

    assert home.exists
    assert home.is_directory
    assert home.user == app_user
    assert home.group == app_user
    assert home.mode == 0o755


def test_app_python(host):
    python = host.file(
        '/home/%s/.pyenv/versions/%s/bin/python%s'
        % (app_user, python_version, python_major_minor_version))

    assert python.exists
    assert python.is_file
    assert python.user == app_user
    assert python.group == app_user
    assert python.mode == 0o755


def test_app_current_link(host):
    expected_deployment = '/home/%s/releases/%s' \
        % (app_user, deployment_version)
    current = host.file('/home/%s/current' % app_user)

    assert current.exists
    assert current.is_symlink
    assert current.user == 'pycsw'
    assert current.group == 'pycsw'
    assert current.linked_to == expected_deployment


def test_app_release_dir(host):
    src = host.file(
        '/home/%s/releases/%s' % (app_user, deployment_version))

    assert src.exists
    assert src.is_directory
    assert src.user == 'pycsw'
    assert src.group == 'pycsw'
    assert src.mode == 0o755


def test_app_virtualenv_dir(host):
    virtualenv = host.file(
        '/home/%s/releases/%s/.venv' % (app_user, deployment_version))

    assert virtualenv.exists
    assert virtualenv.is_directory
    assert virtualenv.user == 'pycsw'
    assert virtualenv.group == 'pycsw'
    assert virtualenv.mode == 0o755


def test_app_virtualenv_python(host):
    python_path = '/home/%s/releases/%s/.venv/bin/python%s' % \
        (app_user, deployment_version, python_major_minor_version)
    python = host.file(python_path)

    assert python.exists
    assert python.is_symlink
    assert python.user == 'pycsw'
    assert python.group == 'pycsw'


def test_app_os_packages(host):
    assert host.package('libgeos-dev').is_installed
    assert host.package('libpq-dev').is_installed


def test_app_requirements(host):
    pip_packages = host.pip_package.get_packages(
        pip_path='/home/%s/releases/%s/.venv/bin/pip'
        % (app_user, deployment_version))

    assert 'OWSLib' in pip_packages


def test_supervisor_conf(host):
    conf = host.file('/etc/supervisor/conf.d/pycsw.conf')

    assert conf.exists
    assert conf.user == 'root'
    assert conf.group == 'root'
    assert conf.mode == 0o644

    assert conf.contains(
        'command=/home/%s/current/.venv/bin/pycsw-ckan.py' % app_user)


def test_pycsw_worker_services(host):
    pycsw_load = host.supervisor('pycsw-load')

    assert not pycsw_load.is_running
    assert pycsw_load.status == 'STOPPED'


def test_cron(host):
    cron = host.file('/etc/cron.d/pycsw')

    assert cron.exists
    assert cron.user == 'root'
    assert cron.group == 'root'
    assert cron.mode == 0o644
