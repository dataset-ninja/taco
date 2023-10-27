Dataset **TACO** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/h/h/5P/Id2M2NvOzld63yYWHQgqPWwmKRj4g0M5lzLfjekV0YaA9nhls2Szj8zI52tm0qX0QYAxeg0e6jhHUhjiPH2kTqt7jOO2jqY5u7a9KAveqps58cgNyf9rvQwHxG1K.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='TACO', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://github.com/pedropro/TACO).