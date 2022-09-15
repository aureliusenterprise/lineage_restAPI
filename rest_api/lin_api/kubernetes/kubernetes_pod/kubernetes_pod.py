import asyncio
import logging
from flask import request
from flask_restx import Resource
from m4i_atlas_core import get_entities_by_type_name, create_entities

from .kubernetes_pod_model import KubernetesPod
from .kubernetes_pod_serializers import m4i_kubernetes_pod_model as kubernetes_pod_serializer
from ... import api, m4i_output_model, m4i_output_get_model, output_filter_functions

""" 
Defining kubernetes_pod, (Python Script) NameSpace
"""
log = logging.getLogger(__name__)
ns = api.namespace('kubernetes/kubernetes_pod', description='Operations related to Kubernetes Pod')


@ns.route("/")
class kubernetes_pod_Class(Resource):

    @api.response(200, 'Kubernetes Pod Entities in Atlas')
    @api.response(400, 'Kubernetes Pod is not Defined in Atlas')
    @api.doc(id='get_kubernetes_pod_entities')
    @api.marshal_with(m4i_output_get_model)
    def get(self):
        """
        Returns list of Kubernetes Pod Entities
        """
        search_result = asyncio.run(get_entities_by_type_name("m4i_kubernetes_pod"))
        transformed_response = output_filter_functions.transform_get_response(search_result)
        return transformed_response, 200

    @api.response(200, 'Kubernetes Pod Entity successfully created.')
    @api.response(500, "ValueError")
    @api.expect(kubernetes_pod_serializer, validate=True)
    @api.doc(id='post_kubernetes_pod_entities')
    @api.marshal_with(m4i_output_model)
    def post(self):
        """
        Creates a new Kubernetes Pod Entity.
        """
        obj = KubernetesPod.from_dict(request.json)
        entity = obj.convert_to_atlas()
        data_read_response = asyncio.run(create_entities(entity))
        transformed_response = output_filter_functions.transform_post_response(data_read_response)
        return transformed_response, 200
