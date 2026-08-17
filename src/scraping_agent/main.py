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

import asyncio
import argparse
from scraping_agent.agent.runner import run_agent, get_system_prompt
from scraping_agent.llm.ollama import get_ollama_llm
from scraping_agent.browser.session import get_browser_session

async def async_main(model: str, prompt: str) -> None:
    llm = get_ollama_llm(model=model)
    browser = get_browser_session(headless=True)
    result = await run_agent(task=prompt, llm=llm, browser=browser, extend_system_message=get_system_prompt())
    print(result)

def main() -> None:
    parser = argparse.ArgumentParser(description="Web scraping and search agent")
    _ = parser.add_argument("--model", "-m", type=str, required=True, help="Ollama model name")
    _ = parser.add_argument("--prompt", "-p", type=str, required=True, help="Task prompt")

    args = parser.parse_args()
    asyncio.run(async_main(model=args.model, prompt=args.prompt))

if __name__ == "__main__":
    main()
