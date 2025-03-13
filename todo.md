1. Tools should have there own usecase instructions and commands.
2. Tools should dictate what is added to the context (not the full output history)
3. Tools should maintain state and have specific commands for mutating state.

When you browse the internet, you do not remember the full state of every webpage you visit.

Instead, you see the current state of webpages and you have memory of the process.

Should we have global tools?
    - make_note, edit_note, and list_notes commands for tracking thoughts and important information

Next:
    - global notes
        - should have a note-state that is open and visible but not inside context
        - can open and close notes at will
    - new program loop that reprompts agent until the task is complete:
        - report to user command
        - get user input command
        - finished task command (same as get user input)
    - create "projects" to work on
    - multiple agents for different projects, possibly have a single controller agent
    - security - having a screening agent.


Bugs:
Make instructions clearer, about what the agent has access too at a given time
When commands are not run correctly it is not added to context.

shell tool needs to update context correctly

