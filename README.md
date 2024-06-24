# fully_on_chain_template
Template for fully on chain model deployment

## Installation
You should put your private key in [config.json](./config.json) and run the following commands to set up the environment:
```bash
# Create the conda environment from the environment.yml file
conda env create -f environment.yml

# Activate the conda environment named 'model_exporter'
conda activate model_exporter

# Install nvm (Node Version Manager) using a remote installation script
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Source the bashrc file to load nvm into the current shell
source ~/.bashrc

# Install Node.js version 20.11.1 using nvm
nvm install 20.11.1

# Install Foundry, a toolkit for Ethereum application development, using a remote installation script
curl -L https://foundry.paradigm.xyz | bash

# Source the bashrc file again to ensure Foundry commands are available in the current shell
source ~/.bashrc

# Update Foundry to the latest version
foundryup

# Clone the specified GitHub repository containing the onchain-keras-2 project
git clone https://github.com/rein-nbc/onchain-keras-2.git
```

## Run
To run deployment, you should run the following command:
```bash
bash run.sh
```