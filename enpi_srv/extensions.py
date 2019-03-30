from flask_restful import Api
from flask_mail import Mail

rest_api = Api(catch_all_404s=True)
mail = Mail()
