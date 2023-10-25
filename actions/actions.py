

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.types import DomainDict
from dotenv import dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}


class ValidateExactInputForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_exactInput_form"
    
    # query flow: tokenIn, amountIn, tokenOut
    def validate_tokenIn(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        slot_value = slot_value.upper()
        print(f"tokenIn registered: {slot_value}")

        # forbid same tokenIn and tokenOut
        # tokenOut = tracker.get_slot("tokenOut")
        # if tokenOut != None:
        #     tokenOut = tokenOut.upper()
        #     if tokenIn != None:
        #         tokenIn = tokenIn.upper()
        #         if tokenIn == tokenOut:
        #             return {"tokenIn": None}
    
        tokenInContract = config.get(slot_value)
        print(f"tokenInContract: {tokenInContract}")
        if tokenInContract!=None:
            # return [SlotSet("tokenInContract",tokenInContract), SlotSet("tokenIn": slot_value)]
            # return [SlotSet("tokenInContract",tokenInContract), SlotSet('tokenIn', slot_value)]
            return {"tokenIn": slot_value, "tokenInContract":tokenInContract}
        
        return {"tokenIn": slot_value} 

       
    
    def validate_amountIn(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print(f"amountIn registered: {slot_value}")
        
        if is_number(slot_value) == False:
            dispatcher.utter_message(text =f"invalid number: {slot_value}")
            return {"amountIn": None}       
        return {"amountIn": slot_value}       
        
    
    def validate_tokenOut(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        slot_value = slot_value.upper()
        print(f"tokenOut registered: {slot_value}")

        # forbid same tokenIn and tokenOut
        # tokenOut = tracker.get_slot("tokenOut")
        # if tokenOut != None:
        #     tokenOut = tokenOut.upper()
        #     if tokenIn != None:
        #         tokenIn = tokenIn.upper()
        #         if tokenIn == tokenOut:
        #             return {"tokenOut": None}

        # config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
        tokenOutContract = config.get(slot_value)
        if tokenOutContract!=None:
            print(f"tokenOutContract: {tokenOutContract}")

            return {"tokenOut": slot_value, "tokenOutContract":tokenOutContract}

        return {"tokenOut": slot_value} 
    
    def validate_tokenInContract(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:    
        print(f"tokenInContract registed: {slot_value}")

        if len(slot_value) != 42:
            dispatcher.utter_message(text =f"invalid contract address: {slot_value}")
            return {"tokenInContract": None} 
        
        return {"tokenInContract": slot_value} 

    def validate_tokenOutContract(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:    
        print(f"tokenOutContract registed: {slot_value}")
        if len(slot_value) != 42:
            dispatcher.utter_message(text =f"invalid contract address: {slot_value}")
            return {"tokenOutContract": None} 
        
        return {"tokenOutContract": slot_value} 

class ActionSubmitExactInputForm(Action):

    def name(self) -> Text:
        return "action_submit_exactInputForm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print(f"form submited")
        response = domain["responses"]["utter_submit_exactInputForm"][0]

        tokenIn = tracker.get_slot("tokenIn")
        tokenOut = tracker.get_slot("tokenOut")
        amountIn = tracker.get_slot("amountIn")
        tokenInContract = tracker.get_slot("tokenInContract")
        tokenOutContract = tracker.get_slot("tokenOutContract")

        response_text = response["text"].format(TokenIn=tokenIn, TokenOut=tokenOut, AmountIn=amountIn, TokenInContract=tokenInContract, TokenOutContract=tokenOutContract)

        dispatcher.utter_message(text =response_text)

          
        return [SlotSet('tokenIn', None), SlotSet('tokenOut', None), SlotSet('amountIn', None), SlotSet('tokenInContract', None), SlotSet('tokenOutContract', None)]

class checkTokenInContract(Action):
    def name(self) -> Text:
        return "action_ask_amountIn"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tokenIn = tracker.get_slot("tokenIn")
        if tokenIn != None:
            dispatcher.utter_message(text =f"How many {tokenIn} you would like to pay")
        return []


class checkTokenInContract(Action):
    def name(self) -> Text:
        return "action_ask_tokenInContract"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tokenIn = tracker.get_slot("tokenIn")
        dispatcher.utter_message(text =f"{tokenIn} contract not found, please input its contract adress:")
    
        return []

class checkTokenOutContract(Action):
    def name(self) -> Text:
        return "action_ask_tokenOutContract"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tokenOut = tracker.get_slot("tokenOut")
        dispatcher.utter_message(text =f"{tokenOut} contract not found, please input its contract adress:")
    
        return []

class ActionClearSlot(Action):
    def name(self) -> Text:
        return "action_clear_allSlot"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [AllSlotsReset()]
def is_number(string):
    try:
        # Try to convert the string to an integer or a float
        int(string)
        return True  # It's an integer
    except ValueError:
        try:
            float(string)
            return True  # It's a float
        except ValueError:
            return False  # It's neither an integer nor a float
   