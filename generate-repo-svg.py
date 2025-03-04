import requests
from textwrap import fill

# GitHub language color mapping
language_colors = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "Java": "#b07219",
    "C++": "#f34b7d",
    "C#": "#178600",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "Go": "#00ADD8",
    "TypeScript": "#2b7489",
    "HTML": "#e34c26",
    "Astro": "#ffb4a1",
    # Add more languages and their colors as needed
}

def get_repo_info(repo_url):
    # Extract the owner and repo name from the URL
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo = parts[-1]

    # Fetch the repository data from GitHub API
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(api_url)
    repo_data = response.json()

    return {
        'name': repo_data['name'],
        'description': repo_data['description'],
        'stars': repo_data['stargazers_count'],
        'language': repo_data['language']
    }

def generate_svg(repo_info):
    # Wrap the description text to fit within the SVG
    wrapped_description = fill(repo_info['description'], width=50)
    description_lines = wrapped_description.split('\n')
    
    # Limit the description to 3 lines and add "..." if there are more lines
    if len(description_lines) > 3:
        description = "\n".join(description_lines[:3]) + "..."
    else:
        description = "\n".join(description_lines)

    # Get the language color from the mapping
    language_color = language_colors.get(repo_info['language'], "#cccccc")

    svg_template = f"""
    <svg width="400" height="150" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" rx="15" ry="15" width="396" height="146" fill="white" stroke="blue" stroke-width="2"/>
        <text x="10" y="30" font-size="18" font-weight="bold" font-family="Arial" fill="#1C3D7E">{repo_info['name']}</text>
    """
    
    # Add the wrapped and limited description to the SVG
    y_position = 60
    for line in description.split('\n'):
        svg_template += f'<text x="10" y="{y_position}" font-size="14" font-family="Arial" fill="#606060">{line}</text>\n'
        y_position += 20
    
    # Add a bit more space before the row with the language and stars
    y_position += 10
    
    # Add the language circle and text only if there is a language
    if repo_info['language']:
        svg_template += f"""
        <circle cx="15" cy="{y_position - 5}" r="6" fill="{language_color}"/>
        <text x="25" y="{y_position}" font-size="14" font-family="Arial" fill="black">{repo_info['language']}</text>
    """
    
    # Add the stars only if there are stars
    if repo_info['stars'] > 0:
        svg_template += f"""
        <text x="115" y="{y_position}" font-size="14" font-family="Arial" fill="black">⭐ {repo_info['stars']}</text>
    """
    
    svg_template += f"""
    </svg>
    """
    return svg_template

# Example usage
repo_url = "https://github.com/your/repository"
repo_info = get_repo_info(repo_url)
svg_content = generate_svg(repo_info)

# Use the repository name for the SVG file name
file_name = f"{repo_info['name']}.svg"

with open(file_name, "w") as file:
    file.write(svg_content)

print(f"SVG file generated as '{file_name}'")