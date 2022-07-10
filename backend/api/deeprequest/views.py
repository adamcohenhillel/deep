"""Deeper 2022, All Rights Reserved
"""
from fastapi import APIRouter, Depends, BackgroundTasks

from api.deeprequest.schemas import DeepRequestSchema
from db.neo4j.entities import DeepRequestNode
from db.session import get_neo4j_connector
from tasks.pipelines import analyze_deep_request

deeprequest_router = APIRouter()


@deeprequest_router.post('/')
async def post(
    body: DeepRequestSchema,
    background_tasks: BackgroundTasks,
    neo4j_connector = Depends(get_neo4j_connector),
):
    """Create a new deep request
    """
    with neo4j_connector.use_session() as session:
        new_node_id = session.write_transaction(
            DeepRequestNode.create,
            body.deep_request
        )
    background_tasks.add_task(
        analyze_deep_request,
        neo4j_connector,
        body.deep_request,
        new_node_id
    )
    return {'node': new_node_id}
