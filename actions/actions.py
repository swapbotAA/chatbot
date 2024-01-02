

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.types import DomainDict
from dotenv import dotenv_values
from .query import getEstimatedAmountOut
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
        if slot_value.isalnum() == False:
            dispatcher.utter_message(text =f"invalid input token: {slot_value}")
            return {"tokenIn": None}    
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

    def validate_minimalAmountOut(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print(f"minimalAmountOut registered: {slot_value}")
         
        # market price
        slot_value = slot_value.upper()
        if slot_value == "Y" or slot_value == "YES":
            return {"minimalAmountOut": 0}  
            return [] 
        
        if slot_value == "N" or slot_value == "NO":
            return {"minimalAmountOut": None, "amountIn":None, "tokenIn":None, "tokenOut":None, "tokenInContract": None, "tokenOutContract": None }  
        # limit order
        if is_number(slot_value) == True:
            return {"minimalAmountOut": slot_value} 
        
               
        dispatcher.utter_message(text =f"unrecognize value: {slot_value}")
        return {"minimalAmountOut": None}            
    
    def validate_tokenOut(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if slot_value.isalnum() == False:
            dispatcher.utter_message(text =f"invalid input token: {slot_value}")
            return {"tokenOut": None}  
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
        minimalAmountOut = tracker.get_slot("minimalAmountOut")
        if minimalAmountOut == 0:
            minimalAmountOut = ""

        tokenInContract = tracker.get_slot("tokenInContract")
        tokenOutContract = tracker.get_slot("tokenOutContract")
        

        response_text = response["text"].format(TokenIn=tokenIn, TokenOut=tokenOut, AmountIn=amountIn,MinimalAmountOut=minimalAmountOut, TokenInContract=tokenInContract, TokenOutContract=tokenOutContract)

        dispatcher.utter_message(text =response_text)

          
        # return [SlotSet('tokenIn', None), SlotSet('tokenOut', None), SlotSet('amountIn', None), SlotSet('tokenInContract', None), SlotSet('tokenOutContract', None)]
        return [AllSlotsReset(None)]

class checkAmountInContract(Action):
    def name(self) -> Text:
        return "action_ask_exactInput_form_amountIn"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tokenIn = tracker.get_slot("tokenIn")
        if tokenIn != None:
            dispatcher.utter_message(text =f"How many {tokenIn} you would like to pay")
        return []

class checkMinimalAmountOut(Action):
    def name(self) -> Text:
        return "action_ask_exactInput_form_minimalAmountOut"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tokenIn = tracker.get_slot("tokenIn")
        amountIn = tracker.get_slot("amountIn")
        tokenOut = tracker.get_slot("tokenOut")
        
        
        # dispatcher.utter_message(text =f"You want to swap {amountIn} {tokenIn} for {tokenOut} at market price? (Y/N), or you can give a specific amount of requested {tokenOut} to make it a limit order")
        
        try:
            estimatedAmountOut = getEstimatedAmountOut(tokenIn,tokenOut,amountIn)
            dispatcher.utter_message(text =f"You want to swap {amountIn} {tokenIn} for estimated {estimatedAmountOut} {tokenOut} at market price? (Y/N), or you can give a specific amount of requested {tokenOut} to make it a limit order")            
            return []
            return {"amountOut": estimatedAmountOut}
        except:
            print("get price failed")
            dispatcher.utter_message(text =f"You want to swap {amountIn} {tokenIn} for {tokenOut} at market price? (Y/N), or you can give a specific amount of requested {tokenOut} to make it a limit order")
            return []


class checkTokenInContract(Action):
    def name(self) -> Text:
        return "action_ask_exactInput_form_tokenInContract"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tokenIn = tracker.get_slot("tokenIn")
        dispatcher.utter_message(text =f"{tokenIn} contract not found, please input its contract adress:")
    
        return []

class checkTokenOutContract(Action):
    def name(self) -> Text:
        return "action_ask_exactInput_form_tokenOutContract"
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
   

# sendTokens

class ValidateSendTokenForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_sendToken_form"
    
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

    def validate_addressOut(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:    
        print(f"recipient registed: {slot_value}")

        if len(slot_value) != 42:
            dispatcher.utter_message(text =f"invalid recipient address: {slot_value}")
            return {"addressOut": None} 
        
        return {"addressOut": slot_value}   
class ActionSubmitSendTokenForm(Action):

    def name(self) -> Text:
        return "action_submit_sendToken_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print(f"form submited")
        response = domain["responses"]["utter_submit_sendToken_form"][0]

        tokenIn = tracker.get_slot("tokenIn")
        addressOut = tracker.get_slot("addressOut")
        amountIn = tracker.get_slot("amountIn")
        tokenInContract = tracker.get_slot("tokenInContract")

        response_text = response["text"].format(TokenIn=tokenIn, AmountIn=amountIn, TokenInContract=tokenInContract, AddressOut=addressOut)

        dispatcher.utter_message(text =response_text)

          
        # return [SlotSet('tokenIn', None), SlotSet('addressOut', None), SlotSet('amountIn', None)]
        return [AllSlotsReset(None)]

class checkSendTokenTokenInContract(Action):
    def name(self) -> Text:
        return "action_ask_sendToken_form_tokenInContract"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tokenIn = tracker.get_slot("tokenIn")
        dispatcher.utter_message(text =f"{tokenIn} contract not found, please input its contract adress:")
    
        return []


# copyTrading

class ValidateCopyTradingForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_copyTrading_form"
    
    # query flow: targetAddress, maximalAmountOfCopyTrading
    def validate_targetAddress(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if len(slot_value) != 42:
            dispatcher.utter_message(text =f"invalid target address: {slot_value}")
            return {"targetAddress": None} 
        return {"targetAddress": slot_value} 

    def validate_maximalAmountOfCopyTrading(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:        
        if is_number(slot_value) == False:
            dispatcher.utter_message(text =f"invalid number: {slot_value}")
            return {"maximalAmountOfCopyTrading": None}       
        return {"maximalAmountOfCopyTrading": slot_value}       
        
class ActionSubmitCopyTradingForm(Action):

    def name(self) -> Text:
        return "action_submit_copyTrading_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print(f"form submited")
        response = domain["responses"]["utter_submit_copyTrading_form"][0]

        targetAddress = tracker.get_slot("targetAddress")
        maximalAmountOfCopyTrading = tracker.get_slot("maximalAmountOfCopyTrading")
    

        response_text = response["text"].format(TargetAddress=targetAddress, MaximalAmountOfCopyTrading=maximalAmountOfCopyTrading)

        dispatcher.utter_message(text =response_text)

          
        # return [SlotSet('tokenIn', None), SlotSet('addressOut', None), SlotSet('amountIn', None)]
        return [AllSlotsReset(None)]
    

# class askCopyTradingTargetAddress(Action):
#     def name(self) -> Text:
#         return "action_ask_copyTrading_form_targetAddress"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         targetAddress = tracker.get_slot("targetAddress")
#         if targetAddress != None:
#             dispatcher.utter_message(text =f"Which address is your target for copy trading?")
#         return []
        
class askCopyMaximalAmountOfCopyTradingAddress(Action):
    def name(self) -> Text:
        return "action_ask_copyTrading_form_maximalAmountOfCopyTrading"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        targetAddress = tracker.get_slot("targetAddress")
            
        if targetAddress != None:
            dispatcher.utter_message(text =f"What is the maximal amount of ETH you would like to pay in each copy trading from {targetAddress}?")
        return []