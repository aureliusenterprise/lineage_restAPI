import asyncio
import logging
from flask import request
from flask_restx import Resource
from m4i_atlas_core import (create_entities, get_entities_by_type_name)
from m4i_backend_core.auth import requires_auth

from .dashboard_Model import Dashboard
from .m4i_dashboard_entity_serializers import m4i_dashboard_entity_model as dashboard_entity_serializer
from ... import output_filter_functions, api, m4i_output_model, m4i_output_get_model, authorizations

""" 
Defining Dashboard Entity
"""
log = logging.getLogger(__name__)
ns = api.namespace('entity/dashboard_entity', description='Operations related to the Dashboard Entity',
                   security='apikey',
                   authorizations=authorizations
                   )


@ns.route("/")
class dashboard_Class(Resource):

    @api.response(200, 'Dashboard Entities in Atlas')
    @api.response(400, 'Dashboard is not Defined in Atlas')
    @api.doc(id='get_dashboard_entities', security='apikey')
    @api.marshal_with(m4i_output_get_model)
    @requires_auth(transparent=True)
    def get(self, access_token=None):
        """
        Returns list of Dashboard Entities
        """
        search_result = asyncio.run(get_entities_by_type_name("m4i_dashboard", access_token=access_token))
        transformed_response = output_filter_functions.transform_get_response(search_result)
        return transformed_response, 200

    @api.response(200, 'Dashboard Entity successfully created.')
    @api.response(500, "ValueError")
    @api.expect(dashboard_entity_serializer, validate=True)
    @api.doc(id='post_dashboard_entities', security='apikey')
    @api.marshal_with(m4i_output_model)
    @requires_auth(transparent=True)
    def post(self, access_token=None):
        """
        Creates a new Dashboard Entity.
        """
        obj = Dashboard.from_dict(request.json)
        entity = obj.convert_to_atlas()
        data_read_response = asyncio.run(create_entities(entity, access_token=access_token))
        transformed_response = output_filter_functions.transform_post_response(data_read_response)
        return transformed_response, 200
