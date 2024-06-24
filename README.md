# fully_on_chain_template
Template for fully on chain model deployment

## Installation
You should put your private key in [config.json](./config.json) and run the following commands to set up the environment:
```bash
# Create the conda environment from the environment.yml file
conda env create -f environment.yml

# Activate the conda environment named 'model_exporter'
conda activate model_exporter
```

## Run
To run deployment, you should run the following command:
```bash
bash run.sh
```