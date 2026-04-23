import yaml
from flasgger import Swagger

def register_swagger(app, swagger):
    """Configura e inicializa Swagger para la aplicación."""
    
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/property",
        "openapi": "3.0.0"
    }
    
    app.config['SWAGGER'] = swagger_config
    
    #base por si el archivo no existe o falla la carga
    swagger_template = {
        "info": {
            "title": "InmoByte API",
            "description": "Documentación de la API",
            "version": "1.0.0"
        }
    }
    
    try:
        with open('app/api/register_and_assign_ownership/swagger.yaml', 'r') as f:
            file_template = yaml.safe_load(f)
            if file_template:
                swagger_template.update(file_template)
    except Exception:
        pass
    
    swagger.template = swagger_template
        
    swagger.init_app(app)
