import argparse
import os
import sys
import json
from loguru import logger
import tensorflow as tf
from src.exporter import ModelExporter


def parse_args():
    parser = argparse.ArgumentParser()
    #
    parser.add_argument(
        "command",
        action='store',
        type=str,
        choices=[
            'init',
            'export-model',
        ],
        help="primary command to run eai"
    )
    parser.add_argument(
        "--name",
        action='store',
        type=str,
        help="name of the model to export"
    )
    parser.add_argument(
        "--model",
        action='store',
        type = str,
        help="path to the model"
    )
    parser.add_argument(
        "--private-key",
        action='store',
        type=str,
        help="private key for on-chain deployment"
    )
    parser.add_argument(
        "--node-endpoint",
        action='store',
        type=str,
        help="node endpoint for on-chain deployment"
    )

    parser.add_argument(
        "--model-inference-cost",
        action='store',
        type=float,
        help="model inference cost"
    )

    parser.add_argument(
        "--chunk-len",
        action='store',
        type=int,
        help="chunk length for model deployment"
    )

    return parser.parse_known_args()



def initialize(**kwargs):
    logger.info("Exporting model to json ...")
    # load default configs
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(package_dir, 'config.json')
    config = {}
    
    if kwargs['private-key'] is None:
        logger.warning('--private-key must be provided for command "eai to-json"')
        sys.exit(2)
    else:
        config["private_key"] = kwargs['private-key']

    if kwargs['node-endpoint'] is None:
        config["node_enpoint"] = "http://127.0.0.1:8545/"
    else:
        config["node_enpoint"] = kwargs['node-endpoint']
    
    if kwargs['model-inference-cost'] is None:
        config["model_inference_cost"] = 0
    else:
        config["model_inference_cost"] = kwargs['model-inference-cost']
    
    if kwargs['chunk-len'] is None:
        config["chunk_len"] = 30000
    else:
        config["chunk_len"] = kwargs['chunk-len']
    with open(config_path, 'w') as fid:
        json.dump(config, fid)
    
def export_model(**kwargs):
    """
    init the configurations for eai deployment
    """
    logger.info('initializing eai deployment ...')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base_dir, 'config.json'), 'r') as fid:
        config = json.load(fid)
    if kwargs['model'] is None:
        logger.warning('--model must be provided for command "eai init"')
        sys.exit(2)
    model_name = ""
    if kwargs['name'] is not None:
        model_name = kwargs['name']
    
    save_dir = os.path.join(base_dir, "outputs")
    # load tensorflow model from keras format
    model = tf.keras.models.load_model(kwargs['model'])
    exporter = ModelExporter()
    exporter.export_model(model, model_name = model_name, output_dir = save_dir)
    logger.info("Creating .env file")
    env_config = {
        "PRIVATE_KEY": config["private_key"],
        "NODE_ENDPOINT": config["node_endpoint"],
        "MODEL_INFERENCE_COST": config["model_inference_cost"],
        "CHUNK_LEN": config["chunk_len"],
        "MODEL_JSON": os.path.join("outputs", "graph.json"),
        "WEIGHT_TXT": os.path.join("outputs", "weights.txt"),
    }
    with open(os.path.join(base_dir, ".env"), "w") as f:
        for key, value in env_config.items():
            f.write(f"{key}={value}\n")
    logger.info(".env file created")


@logger.catch
def main():
    known_args, unknown_args = parse_args()
    for arg in unknown_args:
        logger.warning(f'unknown command or argument: {arg}')
        sys.exit(2)

    # handle different primaryc commands
    if known_args.command == 'init':
        # initialization
        args = {
            'private-key': known_args.private_key,
            'node-endpoint': known_args.node_endpoint,
            'model-inference-cost': known_args.model_inference_cost,
            'chunk-len': known_args.chunk_len
        }
        initialize(**args)
    elif known_args.command == "export-model":
        # export model to json
        args = {
            'name': known_args.name,
            'model': known_args.model
        }
        export_model(**args)

if (__name__ == "__main__"):
    main()
