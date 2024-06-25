# fully_on_chain_template
Template for fully on chain model deployment

## Installation
To install the necessary dependencies, follow these steps:

```bash
# Create the conda environment from the environment.yml file
conda env create -f environment.yml

# Activate the conda environment named 'model_exporter'
conda activate model_exporter

# Clone the specified GitHub repository containing the onchain-keras-2 project
git clone https://github.com/rein-nbc/onchain-keras-2.git
```
or
```bash
bash set_up.sh
```

## Run
To run the deployment, make sure to update the [config.json](./config.json) file with your private key, model h5 file, and model name. Then, execute the following command:

```bash
bash run.sh
```

Note: The code is based on tensorflow 2.16.1. It is recommended that your model should be defined based on this version.