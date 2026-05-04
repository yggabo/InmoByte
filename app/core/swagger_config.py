swagger_config = {
    'title': 'InmoByte API',
    'uiversion': 3,
    'openapi': '3.0.2',
    'info': {
        'title': 'InmoByte API',
        'version': '1.0',
        'description': 'API for real estate management system'
    },
    'specs': [
        {
            "endpoint": 'auth',
            "route": '/auth.json',
            "rule_filter": lambda rule: 'auth' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Auth"
        },
        {
            "endpoint": 'properties',
            "route": '/properties.json',
            "rule_filter": lambda rule: 'property_api' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Properties"
        },
        {
            "endpoint": 'clients',
            "route": '/clients.json',
            "rule_filter": lambda rule: 'clients' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Clients"
        },
        {
            "endpoint": 'appointments',
            "route": '/appointments.json',
            "rule_filter": lambda rule: 'appointments' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Appointments"
        },
        {
            "endpoint": 'agents',
            "route": '/agents.json',
            "rule_filter": lambda rule: 'agents' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Agents"
        },
        {
            "endpoint": 'offers',
            "route": '/offers.json',
            "rule_filter": lambda rule: 'offers' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Offers"
        },
        {
            "endpoint": 'user_profile',
            "route": '/user_profile.json',
            "rule_filter": lambda rule: 'userProfile' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "userProfile"
        },
        {
            "endpoint": 'filters',
            "route": '/filters.json',
            "rule_filter": lambda rule: 'filters_properties' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Filters"
        },
        {
            "endpoint": 'roles',
            "route": '/roles.json',
            "rule_filter": lambda rule: 'roles' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Roles"
        },
        {
            "endpoint": 'property_status',
            "route": '/property_status.json',
            "rule_filter": lambda rule: 'propertyStatus' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "propertyStatus"
        },
        {
            "endpoint": 'status_offers',
            "route": '/status_offers.json',
            "rule_filter": lambda rule: 'statusOffers' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "statusOffers"
        },
        {
            "endpoint": 'main',
            "route": '/main.json',
            "rule_filter": lambda rule: 'main' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Main"
        },
        {
            "endpoint": 'preferences',
            "route": '/preferences.json',
            "rule_filter": lambda rule: 'preferences' in rule.endpoint,
            "model_filter": lambda tag: True,
            "name": "Preferences"
        }
    ],
    'specs_route': '/docs/'
}
