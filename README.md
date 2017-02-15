PA API Client Library
=====================

The PA library provides access to NCC's Performance Analyser API.

## Dependencies

- Python 3.5, 3.6
- urllib3
- certifi

## Installing

You can install this library with pip like so:

```
pip install paapi
```

Or by running `setup.py` from a checkout of the code:

```
cd paapi
python setup.py install
```

## Quick Start Example

```python
from paapi import PaAuth, PaApi

auth = PaAuth('username', 'password', 'basic_auth')
realm = 12345
api = PaApi(auth, realm)

job_templates = api.get_all_jobtemplates()

for job_template in job_templates:
    testruns = api.get_testruns_for_jobtemplate(job_template['sref'])
    for testrun in testruns:
        print(testrun['downloadDuration'])

```

## License

See the [LICENSE](LICENSE) file for more info.
