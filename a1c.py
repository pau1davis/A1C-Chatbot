from langchain.schema import HumanMessage
import streamlit as slit
from langchain.llms import OpenAI
from langchain import Prompt, PromptTemplate
from langchain.chat_models import ChatOpenAI
import json
import requests

def load_llm():
    llm=ChatOpenAI(temperature=.9,openai_api_key='', model="gpt-3.5-turbo-0613",verbose=True)
    return llm
#API key is hard coded so put your own or use environment
llm = ChatOpenAI(temperature=0,openai_api_key='', model="gpt-3.5-turbo-0613", request_timeout=120,verbose=True)

slit.set_page_config(page_title="A1C Order Generator", page_icon=":robot:")

slit.header("A1C Order Generator")

def get_text():
    input_text = slit.text_area (label= "Put your lab result here:",placeholder= "Lab result...", key = "lab_result")
    return input_text
interests_input = get_text()

arguement = """'Listed is a FHIR lab result for glucose:"""+interests_input+"""Store the glucose number. Then store the values for the code and the high and low values. Only if the glucose is greater than 200, then generate a FHIR order for A1C by replacing the blank values of the code below with data from the lab result. Do not make up any values. Do not print anything except the FHIR order.

{'type' : 'object',"resourceType": "ServiceRequest","id": "","category": "" [{"coding": [{ "system": "" ,"code": "" ,"display": "" }]}]"code": {"coding": [{"system": "","code": "","display": ""}],"text": "},"effectiveDateTime": "","issued": "","valueQuantity": {"value": ,"unit": "","system": "","code": ""},"interpretation": [{"coding": [{"system": "","code": "","display": ""}],"text": ""}],"referenceRange": [{"low": {"value": ,"unit": "","system": "","code": ""},"high": {"value": ,"unit": "","system": "","code": ""}]}}"""

arguement2 = """Listed is a FHIR lab result for glucose:"""+interests_input+"""Your goal is to: Store the glucose level. Evaluate if the glucose level is greater than 200. If the glucose level is greater than 200 produce a FHIR order. If it is not, then do not produce a FHIR order."""

if interests_input:

  message = llm.predict_messages([HumanMessage(content = arguement)])

slit.markdown("### Your FHIR Order")

url = 'http://hapi.fhir.org/baseR4/ServiceRequest?_format=json&_pretty=true'
headers = {'Accept-Charset': 'utf-8', 'Accept': 'application/fhir+json;q=1.0, application/json+fhir;q=0.9',
'User-Agent': 'HAPI-FHIR/6.7.8-SNAPSHOT (FHIR Client; FHIR 4.0.1/R4; apache)',
'Accept-Encoding': 'gzip',
'Content-Type': 'application/fhir+json; charset=UTF-8'}

payload = message
slit.write(payload.content)
response = requests.post(url, headers=headers, data=(payload.content[payload.content.index('{'):]), verify=False)