import asyncio
import logging
from flask import request
from flask_restx import Resource
from m4i_atlas_core import (create_entities, get_entities_by_type_name)

from .m4i_elasticIndex_entity_serializers import m4i_elasticIndex_entity_model as elasticIndex_entity_serializer
from .model.ElasticIndexApiModel import ElasticIndexApiModel
from ... import output_filter_functions, m4i_output_model, m4i_output_get_model, api

""" 
Defining elasticIndex  Entity
"""
log = logging.getLogger(__name__)
ns = api.namespace('entity/elasticIndex_entity', description='Operations related to the elasticIndex Entity')


@ns.route("/")
class dashboard_Class(Resource):

    @api.response(200, 'elasticIndex Entities in Atlas')
    @api.response(400, 'elasticIndex is not Defined in Atlas')
    @api.doc(id='get_elasticIndex_entities')
    @api.marshal_with(m4i_output_get_model)
    def get(self):
        """
        Returns list of elasticIndex Entities
        """
        search_result = asyncio.run(get_entities_by_type_name("m4i_elastic_index"))
        transformed_response = output_filter_functions.transform_get_response(search_result)
        return transformed_response, 200

    @api.response(200, 'elasticIndex Entity successfully created.')
    @api.response(500, "ValueError")
    @api.response(204, "ElasticIndex already Exists")
    @api.expect(elasticIndex_entity_serializer)
    @api.doc(id='post_elasticIndex_entities')
    @api.marshal_with(m4i_output_model)
    def post(self):
        """
        Creates a new elasticIndex Entity.
        """
        obj = ElasticIndexApiModel.from_dict(request.json)
        entity, ref = obj.convert_to_atlas()
        data_read_response = asyncio.run(create_entities(*entity, referred_entities=ref))
        transformed_response = output_filter_functions.transform_post_response(data_read_response)
        return transformed_response, 200
