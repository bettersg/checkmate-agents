# checkmate-agents

CheckMate's factchecking agents

# What is this about?

[CheckMate](https://checkmate.sg) is a system where users in Singapore send in dubious messages, and a pool of volunteers vote on messages that our classifier cannot handle. More details can be found [in this post](https://medium.com/@bingwentan/from-start-to-checkmate-a140a4e9c8f9). We are now accepting autonomous factchecking agents into the pool as well.

# What must the agent do?

The agent should be defined in the `CheckerAgent` class in `/implementation/agent.py`. You need to provide a `check_message` method, of which a skeleton already exists. This method will receive an object of the `MessagePayload` class, as defined in `base/schemas.py`. This comprises the following fields:

- messageId - Unique identifier for the message. Can be ignored for the agent's implementation
- type - Either 'image' or 'text'. Used to distinguish different types of messages in the pipeline
- text - Only exists if the message type is 'text'. Text contents of the whatsapp message sent in
- caption - Only exists if the message type is 'image'. The caption of the image sent in
- storageUrl - Only exists if the message type is 'image'. The GCP Cloud Storage Bucket URI of the image sent in. Don't use this for now

The method must return a Vote object, again defined in `base/schemas.py`, which should include the following 2 fields:

- category - Either of the following 7 categories:

  | Category   | Description                                                                                                                                                                               |
  | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | scam       | Intended to obtain money/personal information via deception                                                                                                                               |
  | illicit    | Other potentital illicit activity that are not scams, e.g. moneylending or prostitution                                                                                                   |
  | info       | Messages intended to inform/convince/mislead a broad base of people                                                                                                                       |
  | satire     | Similar to info, but clearly satirical in nature                                                                                                                                          |
  | spam       | Unsolicited spam, such as marketing messages                                                                                                                                              |
  | legitimate | Legitimate source, typically meant for the individual as opposed to a broad base, and can't be assessed without knowledge of the individual's circumstances, e.g. transactional messages. |
  | irrelevant    | Trivial/banal messages with nothing to assess                                                                                                                                             |
  | unsure     | You're unsure of what it is                                                                                                                                                               |

- truthScore - An integer from 1 to 5, where 1 is entirely false and 5 is entirely true. This should only be provided when the category is "info". Otherwise, set truthScore to `None`.

# How to go about creating the agent?

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

# What will happen once your agent is accepted

1. Once your agent is accepted, the agent will receive the same messages as the human voters, as well as other agents, in the voting pool. Their votes will be recorded as well.
