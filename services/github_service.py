import requests
import os
import base64
import json
from concurrent.futures import ThreadPoolExecutor

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# --- DETECTION SIGNATURES ---
TECH_SIGNATURES = {
    # Frameworks
    "Django": ["manage.py", "wsgi.py"],
    "Flask": ["app.py", "wsgi.py"],
    "React": ["next.config.js", "vite.config.js", "react-scripts"],
    "Vue": ["vue.config.js", "nuxt.config.js"],
    "Docker": ["Dockerfile", "docker-compose.yml"],
    "AWS": ["serverless.yml", "cdk.json"],
    
    # Databases
    "MongoDB": ["mongoose", "pymongo", "mongodb"],
    "PostgreSQL": ["psycopg2", "pg", "sequelize", "typeorm"],
    "MySQL": ["mysql2", "mysql-connector", "pymysql"],
    "Redis": ["redis", "ioredis"],
    "Firebase": ["firebase", "firebase-admin"]
}

# --- NEW: COMPETITIVE PROGRAMMING KEYWORDS ---
CP_KEYWORDS = ["leetcode", "codeforces", "hackerrank", "algo", "dsa", "solutions", "competitive", "cp", "interview"]

def get_file_content(username, repo, path):
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return base64.b64decode(response.json()['content']).decode('utf-8')
    except: pass
    return None

def detect_cp_repo(repo_name, files):
    """
    Checks if a repo is likely a Competitive Programming / DSA dump.
    """
    # 1. Check Repo Name (Strong Signal)
    if any(kw in repo_name.lower() for kw in CP_KEYWORDS):
        return True

    # 2. Check File Extensions (Weak Signal, but useful)
    # If repo has .cpp files but NO build system (CMake, Makefile), it's likely CP.
    cpp_files = [f for f in files if f.endswith('.cpp') or f.endswith('.cc')]
    if len(cpp_files) > 0 and "CMakeLists.txt" not in files:
        return True
        
    return False

def scan_repo_tech_stack(username, repo):
    """
    Scans for Frameworks, Databases, AND Competitive Programming.
    """
    detected_tech = []
    
    # 1. Fetch file list
    files = []
    try:
        url = f"https://api.github.com/repos/{username}/{repo}/contents"
        files = [f['name'] for f in requests.get(url, headers=HEADERS, timeout=5).json()]
    except: pass

    # 2. Fetch dependencies
    dependencies_text = ""
    if "package.json" in files:
        dependencies_text += get_file_content(username, repo, "package.json") or ""
    if "requirements.txt" in files:
        dependencies_text += get_file_content(username, repo, "requirements.txt") or ""

    # 3. Match Tech Signatures
    for tech, signs in TECH_SIGNATURES.items():
        if any(s in files for s in signs) or any(s in dependencies_text for s in signs):
            detected_tech.append(tech)

    # 4. --- NEW: DETECT COMPETITIVE PROGRAMMING ---
    if detect_cp_repo(repo, files):
        detected_tech.append("Data Structures & Algorithms")
        detected_tech.append("Competitive Programming")
        # Heuristic: If CP is found, assume strong C++/Python/Java core skills
        detected_tech.append("Core Logic (C++/Java/Python)")

    return list(set(detected_tech))

def fetch_github_data(username):
    user_url = f"https://api.github.com/users/{username}"
    user = requests.get(user_url, headers=HEADERS).json()
    if "message" in user and user["message"] == "Not Found":
        return {"error": "User not found"}

    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=15"
    repos = requests.get(repos_url, headers=HEADERS).json()
    
    analyzed_repos = []

    def process_repo(repo):
        if repo.get('fork', False): return None 
        name = repo['name']
        
        # A. Languages
        langs = {}
        try:
            l_url = f"https://api.github.com/repos/{username}/{name}/languages"
            langs = requests.get(l_url, headers=HEADERS, timeout=3).json()
        except: pass

        # B. Tech Stack (Updated with CP detection)
        tech_stack = scan_repo_tech_stack(username, name)
        
        # C. README
        readme = ""
        try:
            r_url = f"https://api.github.com/repos/{username}/{name}/readme"
            r_resp = requests.get(r_url, headers=HEADERS, timeout=3)
            if r_resp.status_code == 200:
                readme = base64.b64decode(r_resp.json()['content']).decode('utf-8')[:600]
        except: pass

        return {
            "name": name,
            "desc": repo['description'],
            "languages": langs,
            "detected_tech": tech_stack,
            "readme_snippet": readme,
            "updated_at": repo['updated_at'].split('T')[0]
        }

    if isinstance(repos, list):
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(process_repo, repos)
        analyzed_repos = [r for r in results if r is not None]

    return {
        "username": username,
        "public_repos": user.get('public_repos'),
        "deep_scan": analyzed_repos
    }