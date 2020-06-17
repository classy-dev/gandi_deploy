from flask import request

from flask_restful import Resource

from Model import db, Transactions, TransactionsSchema, Tickets, TicketsSchema, Secret, SecretSchema

import stripe

import json

from datetime import datetime

transactions_schema = TransactionsSchema(many=True)

transaction_schema = TransactionsSchema()


def convert_park_to_dict(park, OBJ):
    park_dict = {}
    for attr in vars(park):
        if attr == '_sa_instance_state':
            continue
        attr_value = getattr(park, attr)
        if isinstance(attr_value, OBJ):
            point_dict = vars(attr_value)
            park_dict[attr] = point_dict
        else:
            park_dict[attr] = attr_value
    return park_dict


class PaymentResource(Resource):

    @staticmethod

    def post():

        json_data = request.get_json(force=True)
        if not json_data:

            return {'message': 'No input data provided'}, 400

        secret = Secret.query.all()

        secret_data = convert_park_to_dict(secret[0], Tickets)

        stripe_keys = {
            'secret_key': secret_data['secret_key'],
            'publishable_key': secret_data['public_key']
        }

        stripe.api_key = stripe_keys['secret_key']

        response = json.dumps(json_data)

        data = transaction_schema.loads(response)

        print(data['token'])

        customer = stripe.Customer.create(
            email=data['email'],
            source=data['token']
        )

        created_data = stripe.Charge.create(
            customer=customer.id,
            amount=data['amount'],
            currency='MXN',
            description=data['description']
        )

        if created_data['status'] == 'succeeded':

            success_code = created_data['id'].split('_')
            print(success_code[1])

            transaction = Transactions(
                firstname=data['firstname'],
                lastname=data['lastname'],
                phone=data['phone'],
                email=data['email'],
                amount=data['amount'],
                description=data['description'],
                ticket_number=data['ticket_number'],
                code=success_code[1],
                created_at=datetime.now()
            )

            db.session.add(transaction)

            db.session.commit()

            if(data['ticket_number']):

                ticket = db.session.query(Tickets).filter_by(ticket_number=data['ticket_number']).first()

                ticket.ticket_status = 1

                db.session.commit()

            return {'status': 'success', 'data': success_code[1]}, 200

