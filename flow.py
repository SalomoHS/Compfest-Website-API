from .agent import podcastAgent,fileAgent, tools
from .tools import json_parser, generate_dialog, add_bgm
from langchain_core.messages import HumanMessage
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import Annotated
from typing import List
from fastapi import UploadFile
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class ExtendedMessagesState(TypedDict):
    messages: Annotated[list, add_messages]
    topic: str
    language:str
    duration: str
    style: str
    format: str
    bgm: bool
    speakers: List[str]
    file:List[UploadFile]
    file_summary: str
    parsed_ai_response: dict
    result_url: str
    result_url_with_bgm: str


def should_continue(state):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    else:
        return "json_parser"

async def run_ai_agent(topic: str, language: str, 
            duration: str, style: str,
            format: str, bgm: bool,
            speakers: str,
            file:List[UploadFile] = None):
    builder = StateGraph(ExtendedMessagesState)  

    builder.add_node("file_agent",fileAgent)
    builder.add_node("agent",podcastAgent)
    builder.add_node("tools",ToolNode(tools))
    builder.add_node("json_parser", json_parser)
    builder.add_node("generate_dialog", generate_dialog)
    builder.add_node("add_bgm",add_bgm)

    if file:
        builder.add_edge(START,"file_agent")
        builder.add_edge("file_agent","agent")
        
    else:
        builder.add_edge(START,"agent")
    
    builder.add_conditional_edges("agent",should_continue)
    builder.add_edge("tools","agent")
    builder.add_edge("json_parser","generate_dialog")
    # builder.add_edge(START,"generate_dialog")
    if bgm:
        builder.add_edge("generate_dialog","add_bgm")
        builder.add_edge("add_bgm",END)
    else:
        builder.add_edge("generate_dialog",END)
    graph = builder.compile()

    messages = [HumanMessage(content=topic)]
    messages = await graph.ainvoke({"topic": topic, "language":language,
        "duration":duration, "style":style, "format":format,
        "speakers":speakers,
        "file":file,
        "messages":messages, "file_summary":"None"})
    print(messages)
    if bgm:
        return messages['result_url_with_bgm']
    else:
         return messages['result_url']
