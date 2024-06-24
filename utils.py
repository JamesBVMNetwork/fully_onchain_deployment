import json
import importlib

# Function to dynamically import a class
def get_class(module_name, class_name):
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

def check_model_layers(model):
    model_data = json.loads(model.to_json())
    for layer in model_data["config"]["layers"]:
        assert "class_name" in layer, "class_name is required for layer"
        layer_name = layer["class_name"]
        try:
            layer_class = get_class("layers", layer_name)(layer["config"])
        except:
            return False
    return True