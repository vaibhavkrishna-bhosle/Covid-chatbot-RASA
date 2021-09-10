# new setup
pip freeze > uninstall.txt
pip uninstall -r uninstall.txt

# Rasa installation steps
pip install rasa==2.0.2

# run project

## Build the model
rasa train

## run the chatbot 
rasa run -m models --enable-api --cors "*" --debug

## run custom action in seperate terminal 
rasa run actions

## run for online use
./ngrok http 5005

# Usefull Credentials

http://64d4-49-206-1-206.ngrok.io/webhooks/twilio/webhook


