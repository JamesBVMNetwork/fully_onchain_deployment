# This repository supports EAI's users to deploy their own AI models on-chain.
## Installation

```bash
git clone https://github.com/JamesXYZT/fully_onchain_deployment
cd fully_onchain_deployment
pip install -r requirements.txt
pip install -e .
```

## Usage
After successful installation, you should take the following steps to export your model to json format prepareing for deploying on-chain.
```bash
git clone https://github.com/rein-nbc/onchain-keras-2
cd onchain-keras-2
eai init --private-key $PRIVATE_KEY
eai export-model --model $MODEL_PATH --name $MODEL_NAME
```
Then you can deploy your model on-chain by following the instructions:
```bash
npm install
npm run deployFunctionalModelNew
```