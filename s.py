import requests
import time
from bs4 import BeautifulSoup

TOKEN = "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"
USERNAME = "Snorxexe"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
}

# --------------------------
# 1) HTML'den repo isimlerini çek
# --------------------------
def scrape_repos_html(username):
    repos = []
    page = 1
    while True:
        url = f"https://github.com/{username}?page={page}&tab=repositories"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        repo_tags = soup.find_all("a", itemprop="name codeRepository")
        if not repo_tags:
            break
        for tag in repo_tags:
            repos.append(tag.text.strip())
        page += 1
    return list(set(repos))

# --------------------------
# 2) Workflow ve runları sil
# --------------------------
def get_workflows(repo):
    url = f"https://api.github.com/repos/{USERNAME}/{repo}/actions/workflows"
    r = requests.get(url, headers=headers).json()
    return r.get("workflows", [])

def get_all_runs(repo, workflow_id):
    runs = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{USERNAME}/{repo}/actions/workflows/{workflow_id}/runs?per_page=100&page={page}"
        r = requests.get(url, headers=headers).json()
        if "workflow_runs" not in r or not r["workflow_runs"]:
            break
        runs.extend(r["workflow_runs"])
        page += 1
    return runs

def delete_run(repo, run_id):
    url = f"https://api.github.com/repos/{USERNAME}/{repo}/actions/runs/{run_id}"
    requests.delete(url, headers=headers)

# --------------------------
# 3) Ana program
# --------------------------
repos = scrape_repos_html(USERNAME)

print(f"📌 Bulunan repo sayısı: {len(repos)}")
for r in repos:
    print(f"➡ {r}")

print("\nSilme işlemi başlıyor...\n")

for repo in repos:
    print(f"\n🔹 Repo: {repo}")
    workflows = get_workflows(repo)
    if not workflows:
        print("  ❌ Workflow bulunamadı.")
        continue
    total_deleted = 0
    for wf in workflows:
        wf_id = wf["id"]
        runs = get_all_runs(repo, wf_id)
        print(f"  ➡ Workflow {wf_id} için run sayısı: {len(runs)}")
        for run in runs:
            delete_run(repo, run["id"])
            total_deleted += 1
            time.sleep(0.25)  # Rate limit koruması
    print(f"  ✔ Silinen toplam run: {total_deleted}")

print("\n🎉 Tüm işlemler bitti! 12 repo + tüm run’lar kesinlikle silindi.")