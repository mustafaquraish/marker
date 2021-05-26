from .markus import Markus
from .canvas import Canvas

class LMSFactory:
    __mapping = {}

    @staticmethod
    def register(cls, name, required_params=["lms"]):
        LMSFactory.__mapping[name] = (cls, required_params)
    
    @staticmethod
    def create(config):
        if "lms" not in config:
            raise ValueError(f"config does not have `lms` defined.")
        name = config["lms"]
        if name not in LMSFactory.__mapping:
            raise ValueError(f"LMS name `{name}` not found.")
        cls, required_params = LMSFactory.__mapping[name]
        for param in required_params:
            if param not in config or config[param] is None:
                raise ValueError(f"config[{param}] is missing or null.")
        
        # Clean URL:
        if config["base_url"] and config["base_url"][-1] == "/":
            config["base_url"] = config["base_url"][:-1]

        return cls(config)

LMSFactory.register(Markus, 'markus', ['base_url', 'assignment'])
LMSFactory.register(Canvas, 'canvas', ['base_url', 'course', 'assignment'])