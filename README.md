# Convesational AI
Conversational AI application built using LangChain, Llama2 and Streamlit

## Running this application

1. Clone this repo

    ```bash
    git clone https://github.com/vas610/convesational_ai.git

    cd convesational_ai
    ```

2. Create conda environment

    ```bash
    conda env create -f environment.yml python=3.10  # conda 22.9.0

    conda activate docai

    pip install -r requirements.txt

    python -m ipykernel install --user --name=conda_docai
    ```

3. Download required data

    ```bash
    wget --quiet https://docs.aws.amazon.com/sagemaker/latest/dg/sitemap.xml --output-document - | egrep -o "https://[^<]+" | wget --directory-prefix=./aws_docs/sagemaker/ -i -
    ```

4. Create and Store Embeddings

    ```bash
    ./dataprep.py
    ```

5. Setup a SageMaker Endpoint with Llama2 by following [this](https://aws.amazon.com/blogs/machine-learning/llama-2-foundation-models-from-meta-are-now-available-in-amazon-sagemaker-jumpstart/) blog. I have used the `meta-textgeneration-llama-2-7b-f` model . Also, update the endpoint name in the .env file

6. Run the below command to start the streamlit app

    ```bash
    streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8080 --server.fileWatcherType none --browser.gatherUsageStats False
    ```