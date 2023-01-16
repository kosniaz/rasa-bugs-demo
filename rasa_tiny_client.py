import requests
import json
from urllib import parse
import uuid
import logging

RASA_TIMEOUT=30
RASA_ENDPOINT="webhooks/rest/webhook"



class TinyClient:

    def __init__(self,host="localhost",port="5005"):
        self.host = host
        self.port = port
        self.uuid = uuid.uuid1()

    def tell_rasa(self, msg):
        """Sends a text message to rasa and gets the response.

        Sends an HTTP GET request to Rasa and waits asynchronously for the response. 
        The response is a json string and contains various responses, having 
        a ``text`` field, which is what this function returns. In case of empty text
        fields, an error message is returned to the client.

        Args:
            msg (str) : the text message of the user
        Returns:
            (str) : rasa's response to the user 
        """

        try:
            all_responses=""

            logging.debug(str(self.uuid) + " says '" + 
                         msg + "'. Forwarding to Rasa.")

            requestEndpoint="http://" + self.host+':' + self.port+"/" + RASA_ENDPOINT

            requestBody={'message': msg, 'sender': str(self.uuid)}
            requestBody_json=json.loads(json.dumps(requestBody))
            # adding exceptions for bad statuses 
            # from https://stackoverflow.com/a/16511493
            responseString = requests.post(url = requestEndpoint, json = requestBody_json)
            responseString.raise_for_status()

            appended_responses = [x['text'] for x in responseString.json()]
            all_responses = ''.join(appended_responses)


            if all_responses is None:
                logging.error(
                    "Got None message from rasa. This should not happen.")
                logging.error(ERROR_RASA)
                all_responses = "An error has occured, please close and open the application."
            elif all_responses == "":
                logging.error("Rasa replied an empty string")
                all_responses = "I'm sorry, something went wrong, try again!"
            else:
                logging.debug("Got message from Rasa '" + all_responses + "'")

        except requests.exceptions.ConnectionError as e:
                # HTTPError is raised for non-200 responses; the response
                # can be found in e.response.

            logging.error(str(e))
            all_responses = "The chatbot couldnt be reached, are you sure it is running?"

        return all_responses


    def do_conversation(self):

        print("Starting conversation, say something to your rasa chatbot")
        user_msg=""
        while(True):
            user_msg = input()
            res=self.tell_rasa(user_msg)
            print(res)


    
tc = TinyClient()
tc.do_conversation()
