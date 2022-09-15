import asyncio
import logging
from flask import request
from flask_restx import Resource
from m4i_atlas_core import (create_entities, get_entities_by_type_name)

from .kafkaCluster_Model import KafkaCluster
from .m4i_kafkaCluster_entity_serializers import m4i_kafkaCluster_entity_model as kafkaCluster_entity_serializer
from ... import output_filter_functions, m4i_output_model, m4i_output_get_model, api

""" 
Defining kafkaCluster Entity
"""
log = logging.getLogger(__name__)
ns = api.namespace('entity/kafkaCluster_entity', description='Operations related to the kafkaCluster Entity')


@ns.route("/")
class kafkaCluster_Class(Resource):

    @api.response(200, 'kafkaCluster Entities in Atlas')
    @api.response(400, 'kafkaCluster is not Defined in Atlas')
    @api.doc(id='get_kafkaCluster_entities')
    @api.marshal_with(m4i_output_get_model)
    def get(self):
        """
        Returns list of kafkaCluster Entities
        """
        search_result = asyncio.run(get_entities_by_type_name("m4i_kafka_cluster"))
        transformed_response = output_filter_functions.transform_get_response(search_result)
        return transformed_response, 200

    @api.response(201, 'kafkaCluster Entity successfully created.')
    @api.response(500, "ValueError")
    @api.expect(kafkaCluster_entity_serializer, validate=True)
    @api.doc(id='post_kafkaCluster_entities')
    @api.marshal_with(m4i_output_model)
    def post(self):
        """
        Creates a new kafkaCluster Entity.
        """
        instance = KafkaCluster.from_dict(request.json)
        entity = instance.convert_to_atlas()
        data_read_response = asyncio.run(create_entities(entity))
        transformed_response = output_filter_functions.transform_post_response(data_read_response)
        return transformed_response, 200
