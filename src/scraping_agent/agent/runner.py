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

def get_system_prompt(name : str = "default.md") -> str:
    prompt_path = files("scraping_agent.system_prompt").joinpath(name)
    return prompt_path.read_text(encoding="utf-8")

async def run_agent(task: str, llm: ChatOllama, browser: Browser, extend_system_message: str | None = None, use_thinking: bool = False, use_vision: bool = False, use_judge: bool = False, llm_timeout: int = 300, step_timeout: int = 720, max_actions_per_step: int = 5, max_steps: int = 500):
    agent = Agent(task=task, llm=llm, browser=browser, extend_system_message=extend_system_message, use_thinking=use_thinking, use_vision=use_vision, use_judge=use_judge, llm_timeout=llm_timeout, step_timeout=step_timeout, max_actions_per_step=max_actions_per_step)
    response = await agent.run(max_steps=max_steps)
    return response.final_result()
