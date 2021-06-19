# Rasa installation steps
- conda create --name rasa202
- conda activate base
- conda activate rasa202

- pip install -upgrade pip
- pip install -r install.txt

## Install rasa and rasa-x seperately
- pip installrasa==2.0.2 rasa-x==0.33 -i https://pypi.rasa.com/simple --default-timeout=10000 --use-deprecated=legacy-resolver

## resolve dependencies, if seeing errors.
- pip uninstall attrs kafka-python ujson
- pip install attrs==19.3
- pip install kafka-python==1.4.7
- pip install ujson==1.35


# run project

## Build the model
- rasa train

## run the chatbot
- rasa run -m models --enable-api --cors "*" --debug

## run custom action in seperate terminal
- rasa run actions

## run for online use
- ./ngrok http 5005
