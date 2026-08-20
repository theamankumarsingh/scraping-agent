# Copyright 2026 Aman Kumar Singh

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from importlib.resources import files
from browser_use import Agent, Browser, ChatOllama
from browser_use.llm.messages import UserMessage
from scraping_agent.agent.schema import ResearchResult, ResearchState, IntrospectionResult, PlanningResult

def get_system_prompt(name : str = "system.md") -> str:
    prompt_path = files("scraping_agent.system_prompt").joinpath(name)
    return prompt_path.read_text(encoding="utf-8")

def create_task(state: ResearchState, retry: bool = False) -> str:
    if retry:
        research_template = get_system_prompt("retry.md")
    else:
        research_template = get_system_prompt("research.md")
    new_task = research_template.format(unresolved=state.unresolved, state=state.model_dump_json(indent=2))
    return new_task

def create_introspection_task(state: ResearchState, result: ResearchResult) -> str:
    introspection_template = get_system_prompt("introspection.md")
    new_task = introspection_template.format(objective=state.objective, state=state.model_dump_json(indent=2), result=result.model_dump_json(indent=2))
    return new_task

def create_plan_task(objective: str) -> str:
    plan_template = get_system_prompt("plan.md")
    new_task = plan_template.format(objective=objective)
    return new_task

def check_research_completion(state: ResearchState, max_iterations: int) -> bool:
    if len(state.unresolved) == 0 or state.iterations >= max_iterations:
        return True
    return False

async def run_agent(task: str, llm: ChatOllama, browser: Browser | None = None, extend_system_message: str | None = None, use_thinking: bool = False, use_vision: bool = False, use_judge: bool = False, llm_timeout: int = 300, step_timeout: int = 720, max_actions_per_step: int = 5, max_steps: int = 25, output_model_schema = None):
    agent = Agent(task=task, llm=llm, browser=browser, extend_system_message=extend_system_message, use_thinking=use_thinking, use_vision=use_vision, use_judge=use_judge, llm_timeout=llm_timeout, step_timeout=step_timeout, max_actions_per_step=max_actions_per_step, output_model_schema=output_model_schema, directly_open_url=False)
    response = await agent.run(max_steps=max_steps)
    return response

async def run_introspection(task: str, llm: ChatOllama) -> IntrospectionResult | None:
    try:
        response = await llm.ainvoke([UserMessage(content=task)], output_format=IntrospectionResult)
        return response.completion
    except Exception as e:
        return None

async def run_planning(task: str, llm: ChatOllama) -> PlanningResult | None:
    try:
        response = await llm.ainvoke([UserMessage(content=task)], output_format=PlanningResult)
        return response.completion
    except Exception as e:
        return None

async def research(task: str, llm: ChatOllama, browser: Browser, extend_system_message: str | None = None, use_thinking: bool = False, use_vision: bool = False, use_judge: bool = False, llm_timeout: int = 300, step_timeout: int = 720, max_actions_per_step: int = 5, max_steps: int = 25, max_iterations: int = 5, max_retries: int = 3) -> ResearchState:
    state = ResearchState(objective=task, unresolved=[task])
    current_plan_task = create_plan_task(task)
    planning_result = await run_planning(current_plan_task, llm)
    if planning_result is not None and planning_result.unresolved:
        state.unresolved = planning_result.unresolved
    retry = False
    while not check_research_completion(state, max_iterations):
        current_task = create_task(state, retry)
        research_response = await run_agent(task=current_task, llm=llm, browser=browser, extend_system_message=extend_system_message, use_thinking=use_thinking, use_vision=use_vision, use_judge=use_judge, llm_timeout=llm_timeout, step_timeout=step_timeout, max_actions_per_step=max_actions_per_step, max_steps=max_steps, output_model_schema=ResearchResult)
        research_result = research_response.structured_output
        if research_result is None:
            state.retries += 1
            retry = True
            if state.retries >= max_retries:
                state.iterations += 1
                state.retries = 0
                retry = False
            continue
        state.findings += research_result.findings
        state.visited_urls.update(url for url in research_response.urls() if url and url.startswith(("http://", "https://")))
        state.iterations += 1
        state.retries = 0
        retry = False
        current_introspection_task = create_introspection_task(state, research_result)
        introspection_result = await run_introspection(current_introspection_task, llm)
        if introspection_result is not None:
            current_unresolved = set(state.unresolved)
            filtered_unresolved = [item for item in introspection_result.unresolved if item in current_unresolved]
            if not introspection_result.unresolved or filtered_unresolved:
                state.unresolved = filtered_unresolved
    return state
