import logging

import connexion
from flask_cors import CORS

from utils.configurable_resolver import ConfigurableResolver

logging.basicConfig(level=logging.DEBUG)
app = connexion.App(__name__, specification_dir='./')
CORS(app.app)

# todo: add controllers for keycloak, add prefix depends on env parameter
app.add_api('swagger.yml', resolver=ConfigurableResolver(operation_prefix='controller_noauth.'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

