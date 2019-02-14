#!/usr/bin/env python

import yaml
import intergalactic.settings as settings
import intergalactic.model as model

def print_params(name, p):
  print("%s:"%name)
  for param in p:
    print("   " + str(param) + " = " + str(p[param]))


def load_settings():
    with open("params.yml", "r") as params_file:
        input_params = yaml.safe_load(params_file)

    return settings.validate(input_params)

settings = load_settings()

print_params("Settings", settings)

model = model.Model(settings)
model.run()
