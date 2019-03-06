import argparse, os, shutil, yaml

import intergalactic
import intergalactic.settings as settings
import intergalactic.model as model

def main():
    parser = argparse.ArgumentParser(
        prog="intergalactic",
        description="Command line tools for the intergalactic Python library.",
        epilog="Another dimension, new Galaxy!",
    )
    parser.add_argument("-v", "--version", action="version", version=intergalactic.__version__)
    parser.add_argument("--config", metavar="FILENAME", help="configuration file to use containing model initial params")

    args = parser.parse_args()

    input_params = {}
    if args.config != None:
        with open(args.config, "r") as params_file:
            input_params = yaml.safe_load(params_file)

    context = settings.validate(input_params)

    print("Running model with settings:")
    for param in context:
        print("   " + str(param) + " = " + str(context[param]))

    shutil.rmtree(context['output_dir'], ignore_errors=True)
    if not os.path.exists(context['output_dir']):
        os.makedirs(context['output_dir'])

    model.Model(context).run()
    print(f"Done. Output files ready in '{context['output_dir']}' directory.")
