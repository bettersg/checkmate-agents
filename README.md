# checkmate-agents

CheckMate's factchecking agents

# How to build your own agent

1. Think of a name for your agent, which should have no whitespaces
1. In the repo, create three new branches from base
   - agent/prod/{YOUR_AGENT_NAME}
   - agent/uat/{YOUR_AGENT_NAME}
   - agent/dev/{YOUR_AGENT_NAME}
1. Checkout to agent/dev/{YOUR_AGENT_NAME} branch and begin working on your agent
   1. `pip install -r requirements.txt`
   2. Update {YOUR_AGENT_NAME} in the .agent_name file by replacing TO_FILL
   3. Implement your agent in `implementation/agent.py`. You should modify the `check_message` method. Your implementation must take in a MessagePayload and returns a Vote. You can implement more methods and functions, but make sure that `check_message` method is implemented.
   4. Once implemented, run the command `pytest` from CLI in the root directory. Ensure the unittest passes.
   5. Once done, make a pull request from agent/dev/{YOUR_AGENT_NAME} to agent/uat/{YOUR_AGENT_NAME} and inform the repository owners
   6. Once tested in UAT, make a pull request from agent/uat/{YOUR_AGENT_NAME} to agent/prod/{YOUR_AGENT_NAME} and inform the repository owners
