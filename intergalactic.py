#!/usr/bin/env python

import yaml
import shutil, os
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

def create_output_folder(output_dir):
    shutil.rmtree(output_dir, ignore_errors=True)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


settings = load_settings()
print_params("Running model with settings", settings)

create_output_folder(settings['output_dir'])

model = model.Model(settings)
model.run()

print(f"Done. Output files ready in '{settings['output_dir']}' directory.")
