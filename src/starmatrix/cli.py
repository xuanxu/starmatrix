import argparse
import os
import shutil
import yaml
from os.path import dirname, join, exists

import starmatrix
import starmatrix.settings as settings
import starmatrix.model as model


def main():
    parser = argparse.ArgumentParser(
        prog="starmatrix",
        description="Command line tools for the Starmatrix Python library.",
        epilog="Another dimension, new Galaxy!",
    )
    parser.add_argument("-v", "--version", action="version", version=starmatrix.__version__)
    parser.add_argument("--config", metavar="FILENAME", help="configuration file to use containing model initial params")
    parser.add_argument("--generate-config", action="store_true", help="create a config.yml example file")

    args = parser.parse_args()

    if args.generate_config:
        return create_template_config_file()

    input_params = {}
    if args.config is not None:
        input_params = read_config_file(args.config)

    context = settings.validate(input_params)

    print("Running model with settings:")
    print("")
    for param in context:
        print("   " + str(param) + " = " + str(context[param]))
    print("")

    create_output_directory(context['output_dir'])

    model.Model(context).run()
    print(f"Done. Output files ready in '{context['output_dir']}' directory.")


def create_output_directory(output_dir):
    shutil.rmtree(output_dir, ignore_errors=True)
    if not exists(output_dir):
        os.makedirs(output_dir)


def create_template_config_file():
    shutil.copy(join(dirname(__file__), "sample_input", "params.yml"), "config-example.yml")
    return "Created file: config-example.yml"


def read_config_file(name):
    with open(name, "r") as params_file:
        input_params = yaml.safe_load(params_file)
    return input_params
