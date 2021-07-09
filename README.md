# Rasa installation steps
conda activate rasa
pip install rasa==2.0.2 


# run project

## Build the model
rasa train

## run the chatbot (anaconda)
rasa run -m models --enable-api --cors "*" --debug

## run custom action in seperate terminal (anaconda)
rasa run actions

## run for online use
./ngrok http 5005


https://e30c6adf09e2.ngrok.io/webhooks/twilio/webhook
