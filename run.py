import app as app_module
from app import application

if __name__ == "__main__":
    app_module.register_routes(application)
    application.run(host="0.0.0.0", debug=True)
