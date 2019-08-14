[![CircleCI](https://circleci.com/gh/GSA/datagov-deploy-pycsw.svg?style=svg)](https://circleci.com/gh/GSA/datagov-deploy-pycsw)

# datagov-deploy-pycsw

Ansible role to deploy PyCSW for the Data.gov platform. PyCSW is made up of two
endpoints, `/csw` and `/csw-all`. The difference is that `/csw` applies a filter
to queries, only returning first-order datasets (non-collection members).
`/csw-all` does not apply a filter and includes all datasets, including
collection members.


## Usage

### Dependencies

Include these roles in your requirements.yml.

- [ansistrano.deploy](https://github.com/ansistrano/deploy)
- [avanov.pyenv](https://github.com/avanov/ansible-galaxy-pyenv)

Use the role in your playbook:

```yaml
---
- name: install pycsw
  hosts: pycsw-web
  pre_tasks:
    - name: set pycsw_deploy_version
      set_fact:
	pycsw_deploy_version: "{{ '%Y%m%d%H%M%SZ' | strftime(ansible_date_time.epoch) }}"
  roles:
    - role: gsa.datagov-deploy-pycsw
      vars:
        pycsw_db_password: secret-db-password
        pycsw_db_host: localhost
```


### Variables

This is an incomplete list of supported variables. See `defaults/main.yml` for
more.


#### `pycsw_deploy_version` string required

This is just a timestamp so each deploy can be installed to a unique folder. To
avoid different versions set in the case of using `serial`, it's best to set
this explicitly in your playbook. e.g.

```yaml
- name: deploy
  hosts: all
  pre_tasks:
    - name: set pycsw_deploy_version
      set_fact:
	pycsw_deploy_version: "{{ '%Y%m%d%H%M%SZ' | strftime(ansible_date_time.epoch) }}"
  roles:
    - role: gsa.datagov-deploy-pycsw
```

`pycsw_deploy_version` is passed directly to `ansistrano_release_version`.


#### `pycsw_db_user` string (default: `pycsw`)

The username for the database.


#### `pycsw_db_password` string required

The password for the database.


#### `pycsw_db_host` string required

The username for the database.


#### `pycsw_db_name` string (default: `pycsw`)

The name of the database to use.


#### `pycsw_app_role` string (default: `web`)

One of `web` or `worker`, used to determine which configuration to install.
`web` role runs the web services, `worker` is configured with cron and bulk
loading jobs.


#### `pycsw_app_home` string (default: `/home/pycsw`)

The base directory where the application will be installed.


#### `pycsw_app_repo` string (default: `https://github.com/GSA/pycsw`)

The GitHub repo to pull the application source from.


#### `pycsw_base_url` string (default: `https://catalog.data.gov`)

This roles installs pycsw at two endpoints, `/csw` and `/csw-all`.
`pycsw_base_url` is used as a prefix to these URLs.


#### `pycsw_app_version` string (default: `master`)

The version to fetch from `pycsw_app_repo` during application install.


#### `pycsw_app_os_packages` list of string

List of OS packages required by the application.


#### `pycsw_catalog_url` string (default: `https://catalog.data.gov`)

The URL to use for the catalog service. This is the CKAN instance that will be
scanned for the bulk load job.


#### `pycsw_keep_releases` number (default: 5)

The number of previous releases to keep around. This is passed to
`ansistrano_keep_releases`.


#### `pycsw_python_version` string (default: `2.7.16`)

The version of python to install.


#### `pycsw_support_email` string (default: `datagov@gsa.gov`)

The contact email address to include in the public PyCSW metadata.


## Development

### Requirements

- [Docker](https://www.docker.com/get-started)
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)
- [Python](https://www.python.org) v3.6


### Setup

Pipenv creates a virtualenv for you and installs the python dependencies.

    $ pipenv install --dev

Then you can run commands with pipenv.

    $ pipenv run molecule converge

Or, you can activate the virtualenv in your shell so you don't have to run pipenv
all the time.

    $ pipenv shell


### Run the tests

Run the tests with [molecule](https://molecule.readthedocs.io/en/latest/).

    $ pipenv run molecule test --all

If you're new to molecule, see our
[wiki](https://github.com/GSA/datagov-deploy/wiki/Developing-Ansible-roles-with-Molecule)
for a quick primer.


## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.


## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
