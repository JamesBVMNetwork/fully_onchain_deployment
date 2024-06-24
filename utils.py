import importlib

# Function to dynamically import a class
def get_class(module_name, class_name):
    module = importlib.import_module(module_name)
    return getattr(module, class_name)