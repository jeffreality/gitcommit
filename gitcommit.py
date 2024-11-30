import os
import openai
import json
import subprocess

def load_config():
    """Load the configuration file."""
    config_path = "~/.gitcommit.json"
    with open(os.path.expanduser(config_path), "r") as f:
        return json.load(f)

def get_git_changes():

    """Stage all changes (equivalent to 'git add -A')"""
    try:
        subprocess.run(["git", "add", "--all"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error staging changes: {e.stderr.strip()}")
        exit(1)

    """Get a summary of changes added to the staging area."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.strip()}")
        exit(1)

def generate_commit_message(changes_summary):
    """Generate a Git commit message using the OpenAI ChatCompletion API."""
    config = load_config()
    openai.api_key = config.get("api_key")
    response = openai.chat.completions.create(
        model=config.get("model", "gpt-4o"),
        messages=[
            {"role": "system", "content": "You are an expert Git commit message generator."},
            {"role": "user", "content": f"Generate a concise, properly formatted Git commit message based on the following changes:\n{changes_summary}"}
        ],
        max_tokens=config.get("max_tokens", 100),
        temperature=0.7,
    )

    commit_message = response.choices[0].message.content
    commit_message = commit_message.strip("```").strip()
    return commit_message

def create_commit(dry_run=False):
    """Create a Git commit with a generated message."""
    changes_summary = get_git_changes()
    if not changes_summary:
        print("No changes staged for commit.")
        exit(0)

    # print ("\nGit changes:\n")
    # print (changes_summary)
    # print ("\n")


    commit_message = generate_commit_message(changes_summary)
    print("\nGenerated Commit Message:\n")
    print(commit_message)
    print("\n")


    if dry_run:
        print("Dry run mode: not committing.")
        return

    # Prompt the user for confirmation
    confirm = input("Commit this message? (y/N): ").strip().lower()
    if confirm != "y":
        print("Commit canceled.")
        return

    try:
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.strip()}")
        exit(1)

def main():
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Generate Git commit messages with OpenAI.")
    parser.add_argument("--test", action="store_true", help="Preview the commit message without committing.")
    args = parser.parse_args()
    create_commit(dry_run=args.test)

if __name__ == "__main__":
    main()
