import os
from kfp.components import ComponentStore
from kfp.dsl import pipeline
from kfp.v2.compiler import Compiler

# Load components
component_store = ComponentStore(local_search_paths=["components"])

# Define Components
etl_op = component_store.load_component('etl')


# Define pipeline
@pipeline(
    pipeline_root=os.path.join(os.getenv('BUCKET'), 'pipeline_root'),
    name='kf_project',
)
def create_pipeline():
    """ Create the execution pipeline flow 
    """
    # Node 1
    apply_etl = etl_op()


# Compile pipeline and build json package to deploy in Vertex
if __name__ == "__main__":
    Compiler().compile(
       pipeline_func=create_pipeline,
       package_path="kf_pipeline.json"
    )