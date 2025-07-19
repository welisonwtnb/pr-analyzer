import os
from urllib import response
import requests
import argparse
import google.genai as genai
from prompt import generate_prompt

def get_pr_diff(owner: str, repo: str, pr_number: int, token: str) -> str | None:
    """
    Fetches the diff content for a given Pull Request.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        pr_number (int): The Pull Request number.
        token (str): GitHub Token for authentication.

    Returns:
        str | None: The diff content as a string, or None if an error occurs.
    """
    diff_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(diff_url, headers=headers, allow_redirects=True)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error getting diff for {owner}/{repo} PR #{pr_number}: {response.status_code} - {response.text}")
        return None

def post_pr_comment(owner: str, repo: str, pr_number: int, token: str, comment: str) -> requests.Response:
    """
    Posts a comment to a Pull Request.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        pr_number (int): The Pull Request number.
        token (str): GitHub Token for authentication.
        comment (str): The comment content.

    Returns:
        requests.Response: The response object from the API call.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    payload = {"body": comment}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print(f"Comment posted successfully to {owner}/{repo} PR #{pr_number}")
        return response

    print(f"Error posting comment to {owner}/{repo} PR #{pr_number}: {response.status_code} - {response.text}")

    return response

def get_pr_details(owner: str, repo: str, pr_number: int, token: str) -> dict | None:
    """
    Fetches details of a Pull Request, specifically for title.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    
    print(f"Error fetching PR details for {owner}/{repo} PR #{pr_number}: {response.status_code} - {response.text}")
    
    return None

def main():
    parser = argparse.ArgumentParser(description="Analyze a GitHub Pull Request using GenAI.")
    parser.add_argument("--repo-name", required=True, help="Full name of the repository to analyze (e.g., 'owner/repo-name').")
    parser.add_argument("--pr-number", type=int, required=True, help="The Pull Request number to analyze.")
    parser.add_argument("--repo-path", required=True, help="Path to the checked out target repository code.")
    args = parser.parse_args()

    github_token = os.getenv("GITHUB_TOKEN")
    genai_api_key = os.getenv("GENAI_API_KEY")

    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        return
    if not genai_api_key:
        print("Error: GENAI_API_KEY environment variable not set.")
        return

    try:
        owner, repo_name_only = args.repo_name.split("/")
    except ValueError:
        print(f"Error: Invalid --repo-name format. Expected 'owner/repo-name', got '{args.repo_name}'")
        return

    pr_number = args.pr_number
    target_repo_path = args.repo_path

    print(f"--- Analyzing PR #{pr_number} in repository: {owner}/{repo_name_only} ---")
    print(f"Code checked out to: {target_repo_path}")

    pr_details = get_pr_details(owner, repo_name_only, pr_number, github_token)
    if not pr_details:
        return

    pr_title = pr_details.get("title", "No Title Available")

    diff = get_pr_diff(owner, repo_name_only, pr_number, github_token)
    if not diff:
        return

    prompt = generate_prompt(repo_name_only, diff, pr_title, pr_number)

    try:
        client = genai.Client(api_key=genai_api_key)
        result = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt
        )

        ai_comment = result.text
    except Exception as e:
        print(f"Error generating AI content: {e}")
        ai_comment = f"Automated analysis failed: {e}"

    post_pr_comment(owner, repo_name_only, pr_number, github_token, ai_comment)
    print("-" * 80)

if __name__ == "__main__":
    main()
