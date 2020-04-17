import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pycsw_worker_services(host):
    pycsw_load = host.supervisor('pycsw-load')

    assert not pycsw_load.is_running
    assert pycsw_load.status == 'STOPPED'


def test_cron(host):
    cron = host.file('/etc/cron.d/pycsw')

    assert not cron.exists
