import json
import langchain
# from langchain import LLMChain
import os
from dotenv import load_dotenv
load_dotenv()
# from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

def get_template(agent):
    if agent == 'Market Research Assistant':
        template = """Generate a brief report of competitve analysis for competitors {competitors} of my business, includes a brief report on their products, strategies, and market perception. RESPONSE ONLY INCLDUES PLAIN TEXT"""
        input_variables = ['competitors']
    elif agent == 'Lead Generation Assistant':
        template = """Generate a list of potential leads. Finds emails, news, etc. For target {industry} and job {role}. RESPONSE ONLY INCLDUES PLAIN TEXT"""
        input_variables = ['industry', 'role']
    elif agent == 'Automated Sales Outreach Assistant':
        template = """
        Given a list of leads and a brief message template template, then personalizes and schedules email outreach.
        leads: {leads}

        template: {template}
        RESPONSE ONLY INCLDUES PLAIN TEXT
        """
        input_variables = ['leads', 'template']
    elif agent == 'Social Media Assistant':
        template = """Given a short description of a product or event, and generates promotional content tailored to different social media platforms then posts on behalf of the user. RESPONSE ONLY INCLDUES PLAIN TEXT
        Description: {description}"""
        input_variables = ['description']
    else: return None
    return template, input_variables

def lambda_handler(event, context):
    
    # data = json.loads(event.get('body'), {})
    data = event.get('body')
    agent, content = data.get('role'), data.get('content')
    template, input_variables = get_template(agent)
    prompt = PromptTemplate.from_template(
        template=template
    ).format_prompt(**content).to_string()
    if not prompt: return
    r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "user", "content": "You would act as a {agent}. {prompt}".format(agent=agent, prompt=prompt)},
            ]
    )
    return {
        'statusCode': 200,
        'body': r['choices'][0]['message']['content']
    }