from dotenv import dotenv_values
from kfp.v2.dsl import pipeline
from kfp.v2.compiler import Compiler
from kfp.v2 import dsl

config = dotenv_values('.env')


# Define pipeline
@pipeline(
    name='kf-pipeline',
)
def create_pipeline():
    """ Create the execution pipeline flow 
    """
    # Load file from gcs
    dsl.importer(
        artifact_uri = config['URI'],
        artifact_class = dsl.Dataset,
        reimport = True,
    )


# Compile pipeline and build json package to deploy in Vertex
if __name__ == "__main__":
    Compiler().compile(
       pipeline_func=create_pipeline,
       package_path="kf_pipeline.json"
    )