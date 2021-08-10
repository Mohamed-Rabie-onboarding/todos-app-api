import ruamel.yaml
import json
from os import path

in_file = 'swagger.yaml'
out = 'swagger.json'

yaml = ruamel.yaml.YAML(typ='safe')
with open(path.join(path.dirname(__file__), in_file)) as fpi:
    data = yaml.load(fpi)

with open(path.join(path.dirname(__file__), '..', 'swagger-ui', out), 'w') as fpo:
    json.dump(data, fpo, indent=2)
