from dotenv import dotenv_values
# from kfp.dsl import pipeline
from kfp.compiler import Compiler
from kfp.components import load_component_from_file
from kfp import dsl
from google.cloud import aiplatform

config = dotenv_values('.env')

# Load components
# component_store = ComponentStore(local_search_paths=["components"])
etl_op = load_component_from_file("components/etl/component.yaml")
split_data_op = load_component_from_file("components/split_data/component.yaml")
train_model_op = load_component_from_file("components/model/component.yaml")

# Define pipeline
@dsl.pipeline(
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
        input_1 = split_data.outputs['x_train'],
        input_2 = split_data.outputs['y_train'],
    )



# Compile pipeline and build json package to deploy in Vertex
if __name__ == "__main__":
    aiplatform.init(location=config['LOCATION'])

    Compiler().compile(
       pipeline_func = create_pipeline,
       package_path = "kf_pipeline.json"
    )

    job = aiplatform.PipelineJob(
        display_name = 'my_custom_vertex_pipeline',
        template_path='kf_pipeline.json',
        pipeline_root = 'gs://'+config['BUCKET'],
    )

    job.submit()