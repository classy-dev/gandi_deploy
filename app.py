from flask import Blueprint, render_template

from flask_restful import Api

from resources.Login import LoginResource

from resources.Bgcontent import BgcontentResource

from resources.Tickets import TicketsResource

from resources.Payment import PaymentResource

from resources.Transactions import TransactionsResource

from resources.TemplateRender import IndexResource

api_bp = Blueprint('api', __name__)

api = Api(api_bp)

template_bp = Blueprint('template', __name__)

template = Api(template_bp)

template.add_resource(IndexResource, '/')

api.add_resource(LoginResource, '/login')

api.add_resource(BgcontentResource, '/get_bgcontent')

api.add_resource(TicketsResource, '/get_tickets')

api.add_resource(PaymentResource, '/payment')

api.add_resource(TransactionsResource, '/get_transactions/<role_id>')

