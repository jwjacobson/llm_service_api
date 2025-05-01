from django.conf import settings
from importlib import import_module

def get_provider(name):
    config = settings.LLM_PROVIDERS[name]
    module_path, class_name = config["CLASS"].rsplit(".", 1)
    module = import_module(module_path)
    cls = getattr(module, class_name)
    return cls(**{k: v for k, v in config.items() if k != "CLASS"})
