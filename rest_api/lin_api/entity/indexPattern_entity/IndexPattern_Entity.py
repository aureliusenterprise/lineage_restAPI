import asyncio
import logging
from flask import request
from flask_restx import Resource
from m4i_atlas_core import (create_entities, get_entities_by_type_name)

from .indexPattern_Model import IndexPattern
from .m4i_indexPattern_entity_serializers import m4i_indexPattern_entity_model as indexPattern_entity_serializer
from ... import output_filter_functions, m4i_output_model, m4i_output_get_model, api

""" 
Defining Index Pattern Entity
"""
log = logging.getLogger(__name__)
ns = api.namespace('entity/indexPattern_entity', description='Operations related to the Index Pattern Entity')


@ns.route("/")
class IndexPattern_Class(Resource):

    @api.response(200, 'indexPattern Entities in Atlas')
    @api.response(400, 'indexPattern is not Defined in Atlas')
    @api.doc(id='get_indexPattern_entities')
    @api.marshal_with(m4i_output_get_model)
    def get(self):
        """
        Returns list of indexPattern Entities
        """
        search_result = asyncio.run(get_entities_by_type_name("m4i_index_pattern"))
        transformed_response = output_filter_functions.transform_get_response(search_result)
        return transformed_response, 200

    @api.response(200, 'indexPattern Entity successfully created.')
    @api.response(500, "ValueError")
    @api.expect(indexPattern_entity_serializer, validate=True)
    @api.doc(id='post_indexPattern_entities')
    @api.marshal_with(m4i_output_model)
    def post(self):
        """
        Creates a new indexPattern Entity.
        """
        obj = IndexPattern.from_dict(request.json)
        entity = obj.convert_to_atlas()
        data_read_response = asyncio.run(create_entities(entity))
        transformed_response = output_filter_functions.transform_post_response(data_read_response)
        return transformed_response, 200
