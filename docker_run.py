from server import app
from app import create_app
from app.extensions.utils import get_local_ip
from flask import request

app = create_app(debug=True)

if __name__ == "__main__":
    @app.route("/local_ip")
    def local_ip():
        return get_local_ip()

    @app.after_request
    def log_response_info(response):
        app.logger.info('Status: %s %s %s', response.status, request.method, request.endpoint)
        # app.logger.info(request.endpoint, request.method, '%s', response.status)
        return response
    
    app.run(host="0.0.0.0", port=5000)