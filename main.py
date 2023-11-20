from dotenv import dotenv_values
from kfp.v2.dsl import pipeline
from kfp.v2.compiler import Compiler
from kfp.components import ComponentStore
from kfp.v2 import dsl

config = dotenv_values('.env')

# Load components
component_store = ComponentStore(local_search_paths=["components"])
etl_op = component_store.load_component("etl")
split_data_op = component_store.load_component("split_data")
train_model_op = component_store.load_component("model")

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

    # Apply simple ETL in the data
    etl = etl_op(
        input_1 = data.outputs['artifact']
    )

    # Split data step
    split_data = split_data_op(
        input_1 = etl.outputs['output_1']
    )

    # Train on training set
    train_model_op(
        x_train = split_data.outputs['x_train'],
        y_train = split_data.outputs['y_train'],
    )



# Compile pipeline and build json package to deploy in Vertex
if __name__ == "__main__":
    Compiler().compile(
       pipeline_func = create_pipeline,
       package_path = "kf_pipeline.json"
    )