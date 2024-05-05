import click
from utilities.openai import ask_gpt_3_with_chat_completions, client


system_instruction = """You are a helpful assistant that will give me a git branch name.
Keep the branch name short and concise. Keep them meaningful and related to the title

Ticket ID / URL | Title | Expected branch name
https://jira.corp.adobe.com/browse/CH-12345 | [CH-12345] Fix purchase issue | CH-12345-fix-purchase-issue
CH-12345 | Fix paypal issue | CH-12345-fix-paypal-issue
CIS-25 | Fix spacing | CIS-25-fix-spacing
  | fix-typos | fix-typos
T1 | Housekeeping Card: fix 125 critical, 23 high, 2 medium, 1 low | T1-fix-vulnerabilities
JIRA-12345 | Tear down lambda stacks in CXD Tooling and remove jenkins jobs | JIRA-12345-tear-down-lambda-remove-jenkins-jobs
JIRA-12345 | [POP] Past expiration date of current year is accepted without any displayed error message | JIRA-12345-past-expiration-date
"""


@click.command()
@click.argument("task_id")
@click.argument("title")
def main(task_id, title):
    try:
        user_message = f"Now give me branch name for id: {task_id}, title: {title}"
        res = ask_gpt_3_with_chat_completions(system_instruction, user_message)

        print(res)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
