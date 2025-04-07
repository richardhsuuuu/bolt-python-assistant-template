from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, WebSearchTool
from pydantic import BaseModel
import asyncio
from typing import List

class TopicOutput(BaseModel):
    is_valid_topic: bool
    reasoning: str
    topic: str  # tennis, ai, or investing

class ChatResponseOutput(BaseModel):
    response: str
    follow_up_prompt_questions: List[str]

guardrail_agent = Agent(
    name="Topic Guardrail",
    instructions="Check if the user's question is about tennis, AI, or investing. Also, you can ask general question about what this AI agent can do. If not, reject it.",
    output_type=TopicOutput,
)

tennis_agent = Agent(
    name="Tennis Expert",
    handoff_description="Specialist agent for tennis questions",
    instructions="You are an expert on professional tennis. You can search the web and provide up-to-date information about recent match scores, player rankings, and tournament results. Always verify information from reliable sources.",
    tools=[WebSearchTool()],
    output_type=ChatResponseOutput,
)

ai_agent = Agent(
    name="AI Expert",
    handoff_description="Specialist agent for AI developments",
    instructions="You are an expert on artificial intelligence. You can search the web and provide the latest information about AI research, breakthroughs, and industry trends. Always verify information from reliable sources.",
    tools=[WebSearchTool()],
    output_type=ChatResponseOutput,
)

investing_agent = Agent(
    name="Investing Expert",
    handoff_description="Specialist agent for macroeconomic and investing questions",
    instructions="You are an expert on investing and macroeconomics. You deeply understand the current economic environment and can provide insights about tariffs, market trends, and investment strategies. Always verify information from reliable sources.",
    tools=[WebSearchTool()],
    output_type=ChatResponseOutput,
)

async def topic_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(TopicOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_valid_topic,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's question. Only route to tennis, AI, or investing experts.",
    handoffs=[tennis_agent, ai_agent, investing_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=topic_guardrail),
    ],
) 