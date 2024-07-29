import openai
import json
from fastapi import Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.model import WorkflowChat, WorkflowChatMessage
from supertokens_python.recipe.session import SessionContainer
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import uuid
from models.model import CampaignRequest, ContinueChatRequest

openai.api_key = "Input here  "

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_campaign_info(campaign_info, filename='campaign_launch_requirements.json'):
    try:
        with open(filename, 'w') as f:
            json.dump(campaign_info, f, indent=2)
        logger.info("Campaign info saved successfully.")
    except Exception as e:
        logger.error(f"Error saving campaign info: {str(e)}")

def read_campaign_info(filename='campaign_launch_requirements.json'):
    try:
        with open(filename, 'r') as f:
            campaign_info = json.load(f)
            logger.info("Campaign info loaded successfully.")
            return campaign_info
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from the file: {filename}")
    return None

def create_filled_workflow(campaign_info):
    message = f"""
    You are a Dripify campaign launch expert. Your task is to fill out a complete workflow object based on the given campaign information. The workflow object should include all necessary details for launching a campaign in Dripify, including specific actions to perform, their descriptions, and relevant values.

    Campaign information:
    Campaign Type: {campaign_info.get('CampaignType', 'N/A')}
    Campaign Duration: {campaign_info.get('CampaignDuration', 'N/A')}
    Content Type: {campaign_info.get('ContentType', 'N/A')}
    Call To Action: {campaign_info.get('CallToAction', 'N/A')}
    Personalization Level: {campaign_info.get('PersonalizationLevel', 'N/A')}
    A/B Testing Elements: {campaign_info.get('A/BTestingElements', 'N/A')}
    Success Metrics: {campaign_info.get('SuccessMetrics', 'N/A')}

    Please fill out the following workflow object template with appropriate values based on the campaign information:

    {{
      "workFlowName": "Create New Campaign",
      "endGoal": "Boost engagement with a {{CampaignType}} campaign",
      "variables": [
        {{"CampaignType": "{{CampaignType}}"}},
        {{"CampaignDuration": "{{CampaignDuration}}"}},
        {{"ContentType": "{{ContentType}}"}},
        {{"CallToAction": "{{CallToAction}}"}},
        {{"PersonalizationLevel": "{{PersonalizationLevel}}"}},
        {{"A/BTestingElements": "{{A/BTestingElements}}"}},
        {{"SuccessMetrics": "{{SuccessMetrics}}"}}
      ],
      "workFlowServiceName": "Dripify",
      "createdAt": "{{current_utc_time}}",
      "updatedAt": "{{current_utc_time}}",
      "actionsToPerform": [
        {{
          "_id": "f27deb92-5b96-49cd-9c4e-5253308fdd46",
          "actionTitle": "Click on 'Campaigns'",
          "description": "Click on 'Campaigns'",
          "toolUrl": "http://example.com",
          "action": {{
            "type": "click",
            "value": "{{CampaignType}}"
          }},
          "elemPath": "//*[@id='campaigns-link']",
          "eleClass": "aside__nav-link, js-ripple",
          "eleId": "campaigns-link",
          "actionType": "user"
        }},
        {{
          "_id": "d77e43e9-b0e0-4ed7-8d79-86ed71317138",
          "actionTitle": "Click on 'New Campaign'",
          "description": "Click on 'New Campaign'",
          "toolUrl": "http://example.com",
          "action": {{
            "type": "click",
            "value": ""
          }},
          "elemPath": "/html/body/div[1]/div[1]/main/div[1]/div[1]/span/a/span",
          "eleClass": "",
          "eleId": "",
          "actionType": "user"
        }},
        {{
          "_id": "21cc0553-928c-49ef-a91e-e29669bd04e8",
          "actionTitle": "Click on 'Add Leads'",
          "description": "Click on 'Add Leads'",
          "toolUrl": "http://example.com",
          "action": {{
            "type": "click",
            "value": ""
          }},
          "elemPath": "/html/body/div[1]/div[1]/main/div[1]/div/div[2]/div/section/div[2]/button",
          "eleClass": "btn, btn--base",
          "eleId": "",
          "actionType": "user"
        }},
        {{
          "_id": "77896e4e-8af8-4567-9533-d1df007ebe1e",
          "actionTitle": "Click to fill list name",
          "description": "Click to fill list name",
          "toolUrl": "http://example.com",
          "action": {{
            "type": "click",
            "value": "Boost engagement with a {{CampaignType}} campaign"
          }},
          "elemPath": "//*[@id='leadsPackName']",
          "eleClass": "field__input",
          "eleId": "leadsPackName",
          "actionType": "user"
        }},
        {{
          "_id": "89ec2bc0-7cc1-467a-b908-74bcd3cca858",
          "actionTitle": "Fill list name",
          "description": "Fill list name",
          "toolUrl": "http://example.com",
          "action": {{
            "type": "type",
            "value": "Boost engagement with a {{CampaignType}} campaign"
          }},
          "elemPath": "//*[@id='leadsPackName']",
          "eleClass": "field__input",
          "eleId": "leadsPackName",
          "actionType": "user"
        }},
        {{
          "_id": "181dddca-141e-4cb1-b196-68bb10211eaf",
          "actionTitle": "Click to fill your saved search.",
          "description": "Click to fill your saved search.",
          "toolUrl": "http://example.com",
          "action": {{
            "type": "click",
            "value": ""
          }},
          "elemPath": "//*[@id='LinkedInSearch']",
          "eleClass": "field__input",
          "eleId": "LinkedInSearch",
          "actionType": "user"
        }},
        {{
          "_id": "f381b70a-02ee-4ceb-bd1e-bdb0ae7bdad9",
          "actionTitle": "Fill your saved search.",
          "description": "Fill your saved search.",
          "toolUrl": "http://example.com",
          "action": {{
            "type": "fill",
            "value": "{{CampaignType}}-saved-search-url"
          }},
          "elemPath": "//*[@id='LinkedInSearch']",
          "eleClass": "field__input",
          "eleId": "LinkedInSearch",
          "actionType": "user"
        }},
        {{
          "_id": "a5b1c70a-02ee-4ceb-bd1e-bdb0ae7bdad9",
          "actionTitle": "Click on 'Create a list'",
          "description": "Click on 'Create a list'",
          "toolUrl": "http://example.com",
          "action": {{
            "type": "click",
            "value": ""
          }},
          "elemPath": "//*[@id='main']/section/section/div[3]/button[2]",
          "eleClass": "btn btn--primary btn--xlarge btn--addProspect",
          "eleId": "CreateAList",
          "actionType": "user"
        }}
      ]
    }}

    Please fill in all placeholders ({{placeholder}}) with appropriate values based on the campaign information provided. Ensure that the output is a valid JSON object.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": message}
            ],
            temperature=0.7,
        )

        workflow = json.loads(response['choices'][0]['message']['content'])
        
        # Ensure createdAt and updatedAt are set to the current time
        current_time = datetime.utcnow().isoformat() + "Z"
        workflow['createdAt'] = current_time
        workflow['updatedAt'] = current_time
        
        
        return workflow
    
    except Exception as e:
        logger.error(f"Error during OpenAI API call: {str(e)}")
        return None

def save_workflow(workflow, filename='workflow_object.json'):
    try:
        with open(filename, 'w') as f:
            json.dump(workflow, f, indent=2)
        logger.info(f"Filled workflow saved successfully to {filename}")
    except Exception as e:
        logger.error(f"Error saving workflow to file: {str(e)}")

def generate_initial_prompt():
    return ("Hi there! I'm here to help you set up your Dripify campaign. What type of campaign would you like to create? Options include Welcome Series, Product Launch, Customer Re-engagement, etc.")

def trigger_workflow_chat(workflowId: str):
    try:
        initial_question = generate_initial_prompt()
        # Generate a unique ID for the workflow chat
        unique_id = str(uuid.uuid4())
        workflow_chat = WorkflowChat(
            id=unique_id,  # Ensure this is a unique ID
            workflowid=workflowId,
            messages=[WorkflowChatMessage(question=initial_question)],
            collected_info={}
        )
        workflow_chat_data = jsonable_encoder(workflow_chat)
        filename = f"workflow_chat_{unique_id}.json"
    
    except Exception as e:
        print(e)
    
    try:
        with open(filename, 'w') as f:
            json.dump(workflow_chat_data, f, indent=2)
        logger.info(f"Workflow chat saved successfully to {filename}")
    except Exception as e:
        logger.error(f"Error saving workflow chat to file: {str(e)}")
    return {"chat_id": unique_id}

def continue_workflow_chat(request: Request, chatId: str, user_response: str):
    filename = f"workflow_chat_{chatId}.json"
    try:
        with open(filename, 'r') as f:
            workflow_chat_data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Workflow chat not found")

    workflow_chat = WorkflowChat(**workflow_chat_data)
    last_message = workflow_chat.messages[-1]
    last_message.response = user_response

    context = [{"role": "assistant", "content": msg.question} for msg in workflow_chat.messages]
    context.append({"role": "user", "content": user_response})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """
                You are a dripify campaign launch assistant for Dripify (a LinkedIn automation tool).
                Your tasks are to:
                1. Collect user requirements for the campaign launch.
                2. Validate responses and map them to appropriate Dripify categories.
                3. Handle invalid responses by providing valid examples.
                4. Allow modifications to the collected parameters.
                5. Track and complete the setup based on user inputs.
                6. Determine if the user wants to finish the setup(they can use natural language to express like : "No That's it","I think this will do","I think this will fullfill me rewuirements" etc...).
                7. User can use natural language so process and if the response is valid then map it
                """
            },
            *context
        ],
        functions=[
            {
                "name": "update_campaign_info",
                "description": "Update or add campaign launch parameters based on user input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parameter": {"type": "string", "description": "The parameter to update or add"},
                        "value": {"type": "string", "description": "The mapped value for the parameter"},
                        "valid": {"type": "boolean", "description": "Whether the input is valid"},
                        "message": {"type": "string", "description": "Message to display to the user"},
                        "next_question": {"type": "string", "description": "Next question to ask the user"},
                        "finished": {"type": "boolean", "description": "Whether the user wants to finish the process"}
                    },
                    "required": ["parameter", "value", "valid", "message", "next_question", "finished"]
                }
            }
        ],
        function_call={"name": "update_campaign_info"}
    )

    result = json.loads(response.choices[0].message.function_call.arguments)

    if result['valid']:
        workflow_chat.collected_info[result['parameter']] = result['value']
    if result['finished']:
        workflow_chat.is_completed = True
        workflow_chat.json_filename = f"campaign_launch_requirements_{workflow_chat.id}.json"
        with open(workflow_chat.json_filename, 'w') as f:
            json.dump(workflow_chat.collected_info, f, indent=2)

        # Generate and save the filled workflow
        campaign_info = workflow_chat.collected_info
        filled_workflow = create_filled_workflow(campaign_info)
        save_workflow(filled_workflow, filename=f"workflow_{workflow_chat.id}.json")
    
    workflow_chat.messages.append(WorkflowChatMessage(question=result['next_question']))
    workflow_chat_data = jsonable_encoder(workflow_chat)
    with open(filename, 'w') as f:
        json.dump(workflow_chat_data, f, indent=2)
    
    return workflow_chat

def run_dripify_assistant():
    print("Welcome to the Dripify Campaign Launch Assistant!!")
    print("I'm here to help you set up your Dripify campaign.")
    print("You can provide information, ask questions, or modify your choices at any time.")
    print("Let me know when you're finished or satisfied with the requirements.")

    context = []
    collected_info = {}

    initial_prompt = "Hello! I'm excited to help you launch your Dripify campaign. To get started, could you tell me what type of campaign you want to create? For example, Welcome Series, Product Launch, Customer Re-engagement, etc."

    print(f"\nAssistant: {initial_prompt}")

    while True:
        user_input = input("\nUser: ")

        context.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a dripify campaign launch assistant for Dripify(a linkedin automation tool).
                    Your tasks are to:

                            1. **Collect User Requirements:** Start by asking clear and friendly questions to gather details about the campaign launch. Ensure that each question is specific to one parameter at a time.

                            2. **Clarify and Confirm:** If any answers are ambiguous or incomplete, ask follow-up questions to clarify their needs and make sure you have all the necessary information.

                            3. **Map Responses:** Use the reference mapping provided below to convert user responses into the appropriate Dripify categories. Validate their inputs and populate the JSON object accordingly.

                            4. **Handle Invalid Responses:** When encountering invalid answers, offer examples from the allowed values list. Re-ask the question in a helpful manner until you receive a valid response.

                            5. **Allow Modifications:** Users should be able to modify any previously provided parameters. If they request changes, update the existing data as needed.

                            6. **Track and Complete:** Keep track of all information gathered. If any details are missing, ask for those specific pieces to complete the campaign setup according to Dripify’s criteria.

                            7. **Skipping Questions:** Users can skip questions by leaving them blank or explicitly indicating they want to skip. In such cases, map the skipped parameter to a placeholder value or handle it accordingly.

                            8. **Determine Completion:** Monitor user responses for cues indicating they want to finish. If they use phrases like "that's enough" or "I'm done," set 'finished' to true and end the process.


                    Reference mapping for allowed values:
                     - CampaignType: Welcome Series, Product Launch, Customer Re-engagement, Abandoned Cart, Seasonal Promotion, Loyalty Program, Newsletter, Event Invitation
                     - AudienceSegment: New Subscribers, Active Customers, Inactive Customers, High-value Customers, First-time Buyers, Repeat Customers, Abandoned Cart Users
                     - EmailFrequency: Daily, Every Other Day, Twice a Week, Weekly, Bi-weekly, Monthly
                     - CampaignDuration: 3 days, 1 week, 2 weeks, 1 month, 3 months, 6 months, Ongoing
                     - ContentType: Promotional, Educational, Testimonials, Product Updates, Company News, User-generated Content, Behind-the-scenes
                     - CallToAction: Shop Now, Learn More, Book a Demo, Subscribe, Claim Offer, Join Waitlist, RSVP
                     - PersonalizationLevel: Basic (Name), Intermediate (Browsing History), Advanced (Purchase History + Preferences)
                     - A/BTestingElements: Subject Lines, Email Content, Send Times, CTAs, Images, Personalization Level
                     - SuccessMetrics: Open Rate, Click-through Rate, Conversion Rate, Revenue Generated, List Growth Rate, Unsubscribe Rate

                    Example Mapping:
                    - For **CampaignType**: If the user responds with "welcome emails for new customers", map to "Welcome Series".
                    - For **AudienceSegment**: If the user says "people who have bought before", map to "Repeat Customers".
                    - For **EmailFrequency**: If the user mentions "every other day", map to "Every Other Day".
                    - For **CampaignDuration**: If the user specifies "about a month", map to "1 month".
                    - For **ContentType**: If the user indicates "educational content", map to "Educational".
                    - For **CallToAction**: If the user says "get more info", map to "Learn More".
                    - For **PersonalizationLevel**: If the user mentions "using their browsing history", map to "Intermediate (Browsing History)".
                    - For **A/BTestingElements**: If the user refers to "testing different email subjects", map to "Subject Lines".
                    - For **SuccessMetrics**: If the user says "how many people open the emails", map to "Open Rate".
                    - For **EndGoal**: If the user mentions "increase sales of our new product", map to "Boost sales of new product launch".
                    - For **ListName**: If the user says "new product interested customers", map to "New Product Interest List".
                    - For **SavedSearch**: If the user provides "LinkedIn search for tech professionals in California", map to the appropriate LinkedIn search URL or identifier.

                    When a response is invalid, provide the user with specific examples from the mapping list and ask them to provide a valid response. Confirm all parameters with the user and request any additional details as needed. Maintain a smooth conversation flow and ensure the user can update their inputs if necessary. End the process when the user indicates they are finished.
                    """
                },
                {"role": "assistant", "content": initial_prompt},
                *context
            ],
            functions=[
                {
                    "name": "update_campaign_info",
                    "description": "Update or add campaign launch parameters based on user input.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "parameter": {"type": "string", "description": "The parameter to update or add"},
                            "value": {"type": "string", "description": "The mapped value for the parameter"},
                            "valid": {"type": "boolean", "description": "Whether the input is valid"},
                            "message": {"type": "string", "description": "Message to display to the user"},
                            "next_question": {"type": "string", "description": "Next question to ask the user"},
                            "finished": {"type": "boolean", "description": "Whether the user wants to finish the process"}
                        },
                        "required": ["parameter", "value", "valid", "message", "next_question", "finished"]
                    }
                }
            ],
            function_call={"name": "update_campaign_info"}
        )

        result = json.loads(response.choices[0].message.function_call.arguments)

        if result['finished']:
            print(f"Assistant: {result['message']}")
            break

        if result['valid']:
            collected_info[result['parameter']] = result['value']
            print(f"Assistant: {result['message']}")
            if result['next_question']:
                print(f"Assistant: {result['next_question']}")
        else:
            print(f"Assistant: {result['message']}")
            print(f"Assistant: {result['next_question']}")

        context.append({"role": "assistant", "content": result['message'] + " " + result['next_question']})

    print("\nHere's the final collected information:")
    print(json.dumps(collected_info, indent=2))

    with open('campaign_launch_requirements.json', 'w') as f:
        json.dump(collected_info, f, indent=2)

    print("The requirements have been saved to 'campaign_launch_requirements.json'")

    # Generate and save the filled workflow
    filled_workflow = create_filled_workflow(collected_info)
    save_workflow(filled_workflow, filename='workflow_object.json')

    print("The workflow has been generated and saved to 'workflow_object.json'")

def dripify_assistant():
    run_dripify_assistant()

if __name__ == "__main__":
    dripify_assistant()


