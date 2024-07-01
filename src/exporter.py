import os
import json
import struct
import base64
import tensorflow as tf
from loguru import logger
from src.utils import get_class

class ModelExporter:
    def __init__(self):
        pass

    def _export_inbound_nodes_tf_216(self, layer, layer_indices):
        ret = []
        inbound_nodes = layer["inbound_nodes"]
        for node in inbound_nodes:
            inbound_node_data = {"args": [], "kwargs": node["kwargs"]}
            for idx, args in enumerate(node["args"]):
                if isinstance(args, dict):
                    config = args["config"]
                    inbound_node_data["args"].append({
                        "name": config["keras_history"][0],
                        "idx": layer_indices.index(config["keras_history"][0]),
                        "shape": config["shape"],
                    })
                elif isinstance(args, float):
                    inbound_node_data["args"].append(args)
                elif isinstance(args, list):
                    for arg in args:
                        config = arg["config"]
                        inbound_node_data["args"].append({
                            "name": config["keras_history"][0],
                            "idx": layer_indices.index(config["keras_history"][0]),
                            "shape": config["shape"],
                        })
                else:
                    logger.info(f"Type {type(args)} not supported")
                    raise Exception("Inbound node args not supported")
            ret.append(inbound_node_data)
        return ret
    
    def _export_model_graph(self, model, tf_version, output_path=None):
        model_data = json.loads(model.to_json())
        logger.info("Exporting model graph")
        graph = {
            "layers": []
        }
        layer_indices = []
        graph["class_name"] = model_data["class_name"]
        for idx, layer in enumerate(model_data["config"]["layers"]):
            layer_config = layer["config"]
            layer_name = layer_config["name"]
            class_name = layer["class_name"]
            data = {
                "idx": idx,
                "name": layer_name,
                "class_name": class_name,
            }
            try:
                layer_class = get_class("layers", class_name)(layer_config)
                layer_config = layer_class.get_layer_config()
                logger.info(f"Layer {class_name} exported")
            except:
                logger.info(f"Layer {class_name} not supported")
                raise Exception(f"Layer {class_name} not supported")
            data["layer_config"] = layer_config
            layer_indices.append(layer_name)
            if tf_version == "2.16.1":
                if graph["class_name"] == "Functional":
                    data["inbound_nodes"] = self._export_inbound_nodes_tf_216(layer, layer_indices)
            graph["layers"].append(data)
        if output_path:
            with open(output_path, "w") as f:
                json.dump(graph, f)
            logger.info(f"Model graph exported to {output_path}")
        logger.info("Model graph exported")
        return graph
        

    def _export_weights(self, model, output_path = None):
        logger.info("Exporting model weights")
        weights = []
        for layer in model.layers:
            w = layer.get_weights()
            weights.append(w)
        weight_bytes = bytearray()
        for idx, layer in enumerate(weights):
            for weight_group in layer:
                flatten = weight_group.reshape(-1).tolist()
                for i in flatten:
                    weight_bytes.extend(struct.pack("@f", float(i)))
        weight_base64 = base64.b64encode(weight_bytes).decode()
        if output_path:
            with open(output_path, "w") as f:
                f.write(weight_base64)
            logger.info(f"Weights exported to {output_path}")
        logger.info("Weights exported")

    def _export_tf_model(self, model, model_name = None, output_dir = None, tf_version = None):
        logger.info("Exporting Tensorflow/Keras model")
        if tf_version is None:
            tf_version = "2.16.1"
        model_graph_path = None
        weights_path = None
        if output_dir is not None:
            os.makedirs(output_dir, exist_ok=True)
            model_graph_path = os.path.join(output_dir, "graph.json")
            weights_path = os.path.join(output_dir, "weights.txt")
        model_graph = self._export_model_graph(model, tf_version, model_graph_path)
        model_graph["model_name"] = "" if model_name is None else model_name
        weights = self._export_weights(model, weights_path)
        logger.info("Model exported")
        return {
            "model_graph": model_graph,
            "weights": weights
        }

    def export_model(self, model, model_name = None, output_dir = "outputs"):
        model_data = self._export_tf_model(model, model_name, output_dir, tf_version = tf.__version__)
        return model_data