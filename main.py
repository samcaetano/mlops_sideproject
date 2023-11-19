from dotenv import dotenv_values
from kfp.v2.dsl import pipeline
from kfp.v2.compiler import Compiler
from kfp.components import ComponentStore
from kfp.v2 import dsl

config = dotenv_values('.env')

# Load components
component_store = ComponentStore(local_search_paths=["components"])
etl_op = component_store.load_component("etl")

# Define pipeline
@pipeline(
    pipeline_root = config['BUCKET'],
    name = 'kf-pipeline',
)
def create_pipeline():
    """ Create the execution pipeline flow 
    """
    # Load file from gcs
    data = dsl.importer(
        artifact_uri = config['URI'],
        artifact_class = dsl.Dataset,
        reimport = True,
    )

    etl_op(input_1=data.outputs['artifact'])



# Compile pipeline and build json package to deploy in Vertex
if __name__ == "__main__":
    Compiler().compile(
       pipeline_func = create_pipeline,
       package_path = "kf_pipeline.json"
    )