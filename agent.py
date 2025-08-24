from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from .tools import get_speakers, get_topics
import os
from dotenv import load_dotenv
load_dotenv()

base_dir = os.path.dirname(__file__)
prompt_path = os.path.join(base_dir, "prompt.txt")
prompt_1speaker_path = os.path.join(base_dir, "prompt-1speaker.txt")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",google_api_key=os.getenv("GOOGLE_API_KEY")
)

tools = [get_speakers, get_topics]

async def podcastAgent(state):
    system_prompt = None
    if len(state['speakers']) == 2:
        with open(prompt_path,"r") as f:
            system_prompt = f.read()
        
        system_prompt = PromptTemplate.from_template(system_prompt)
        system_prompt = system_prompt.format(
            topic= state['topic'] + " "+ state['file_summary'] if state['file_summary'] else state['topic'],
            duration=state["duration"],
            speaker1=state["speakers"][0],
            speaker2=state["speakers"][1],
            language=state["language"],
            format=state["format"],
            style=state["style"]
        )
        llm_with_tools = llm.bind_tools(tools)
        return {
            "messages": await llm_with_tools.ainvoke([SystemMessage(content=system_prompt)] + state['messages'])
        }
    else:
        with open(prompt_1speaker_path,"r") as f:
            system_prompt = f.read()
        system_prompt = PromptTemplate.from_template(system_prompt)
        system_prompt = system_prompt.format(
            topic= state['topic'] + " "+ state['file_summary'] if state['file_summary'] else state['topic'],
            duration=state["duration"],
            speaker=state["speakers"][0],
            language=state["language"],
            format=state["format"],
            style=state["style"]
        )
        llm_with_tools = llm.bind_tools(tools)
        return {
            "messages": await llm_with_tools.ainvoke([SystemMessage(content=system_prompt)] + state['messages'])
        }

async def fileAgent(state):
    files = [genai.upload_file(i.file,mime_type=i.content_type) for i in state['file']]

    response = model.generate_content([
        *files,
        f"Summarize the content to get the topic detail of {state['topic']}",
        "Return ONLY the sentence of summary",
    ])
    summary = response.parts[0].text
    return {'file_summary': summary}