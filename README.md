# ChatGPT Prompting Guidelines

Based on the course ChatGPT Prompt Engineering for Developers by deeplearning.ai

## Principle 1: Write clear and specific instructions

-  Tactic 1: Use delimiters to clearly indicate distinct parts of the input

- Tactic 2: Ask for a structured output

- Tactic 3: Ask the model to check whether conditions are satisfied

- Tactic 4: "Few-shot" prompting

## Principle 2: Give the model time to “think” 

- Tactic 1: Specify the steps required to complete a task

- Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion

## Ideas

### Iterative
- Better to iterate many times rather than to have the a "perfect prompt"

### Inferring

- Infer information from a text, i.e. sentiment, purpose, name, etc.

### Summarize

- Summarize a text, extract information.

### Transforming

- Stylize a text, translate it, translate code, etc.

### Roles

- OpenAI API admits three roles:
    - system (how the assistant should response / who it is)
    - user (user input)
    - assistant (chatgpt response)