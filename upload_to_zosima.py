#!/opt/anaconda3/envs/default/bin/python3
"""
Automated Upload Script for Zosima.ai Lab 3 Assessment
Student: Sai Nayan Mamilla
"""

import os
import sys
import time
import base64
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES_TO_UPLOAD = [
    {
        "index": 0,
        "question": "Question 1: Implement centralized logging",
        "filename": "Task_01_Implement_Centralized_Logging_ELK.pdf",
        "path": os.path.join(BASE_DIR, "individual_task_pdfs", "Task_01_Implement_Centralized_Logging_ELK.pdf")
    },
    {
        "index": 1,
        "question": "Question 2: Integrate security into the CI/CD pipeline",
        "filename": "Task_02_Integrate_Security_DevSecOps_Pipeline.pdf",
        "path": os.path.join(BASE_DIR, "individual_task_pdfs", "Task_02_Integrate_Security_DevSecOps_Pipeline.pdf")
    },
    {
        "index": 2,
        "question": "Question 3: Set up monitoring using Prometheus",
        "filename": "Task_03_Monitoring_Prometheus_Grafana.pdf",
        "path": os.path.join(BASE_DIR, "individual_task_pdfs", "Task_03_Monitoring_Prometheus_Grafana.pdf")
    },
    {
        "index": 3,
        "question": "Question 4: Implement feature flags and perform different testing",
        "filename": "Task_04_FeatureFlags_LoadTesting_Selenium.pdf",
        "path": os.path.join(BASE_DIR, "individual_task_pdfs", "Task_04_FeatureFlags_LoadTesting_Selenium.pdf")
    },
    {
        "index": 4,
        "question": "Question 5: Prepare a monitoring, logging, and DevSecOps report",
        "filename": "Task_05_Monitoring_Logging_DevSecOps_Report.pdf",
        "path": os.path.join(BASE_DIR, "individual_task_pdfs", "Task_05_Monitoring_Logging_DevSecOps_Report.pdf")
    }
]

def upload_file(idx, fname, fpath):
    if not os.path.exists(fpath):
        print(f"[!] File not found: {fpath}")
        return False

    with open(fpath, "rb") as f:
        b64_str = base64.b64encode(f.read()).decode("ascii")

    print(f"[*] Uploading Q{idx+1}: {fname} ({os.path.getsize(fpath):,} bytes)...")

    inject_js = f"""(function() {{
        try {{
            const b64 = {json.dumps(b64_str)};
            const bin = atob(b64);
            const bytes = new Uint8Array(bin.length);
            for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
            const file = new File([bytes], {json.dumps(fname)}, {{ type: 'application/pdf' }});
            const inps = document.querySelectorAll('input[type=file]');
            if (!inps[{idx}]) return 'ERROR: input not found';
            const dt = new DataTransfer();
            dt.items.add(file);
            inps[{idx}].files = dt.files;
            inps[{idx}].dispatchEvent(new Event('change', {{ bubbles: true }}));
            return 'OK: ' + file.name + ' (' + file.size + ' bytes)';
        }} catch(e) {{
            return 'ERROR: ' + e.message;
        }}
    }})()"""

    jxa = f"""
    const Chrome = Application('Google Chrome');
    let targetTab = null;
    for (const w of Chrome.windows()) {{
        for (const t of w.tabs()) {{
            if (t.url().includes('lab-assessment-start')) {{
                targetTab = t;
                break;
            }}
        }}
        if (targetTab) break;
    }}

    if (!targetTab) {{
        'ERROR_NO_ZOSIMA_TAB';
    }} else {{
        targetTab.execute({{ javascript: {json.dumps(inject_js)} }});
    }}
    """

    proc = subprocess.run(['osascript', '-l', 'JavaScript'], input=jxa, text=True, capture_output=True)
    out = proc.stdout.strip()
    print(f"    -> Response: {out}")
    return "OK:" in out

def check_portal_status():
    jxa = """
    const Chrome = Application('Google Chrome');
    let targetTab = null;
    for (const w of Chrome.windows()) {
        for (const t of w.tabs()) {
            if (t.url().includes('lab-assessment-start')) {
                targetTab = t;
                break;
            }
        }
        if (targetTab) break;
    }

    if (!targetTab) {
        'ERROR_NO_ZOSIMA_TAB';
    } else {
        const inspectJs = `(function() {
            const listItems = Array.from(document.querySelectorAll("li"));
            const files = listItems.map(li => {
                const a = li.querySelector("a");
                return {
                    name: a ? a.innerText.trim() : "Unknown",
                    uploaded: li.innerText.includes("Uploaded")
                };
            });
            return JSON.stringify(files);
        })()`;
        targetTab.execute({ javascript: inspectJs });
    }
    """
    proc = subprocess.run(['osascript', '-l', 'JavaScript'], input=jxa, text=True, capture_output=True)
    try:
        data = json.loads(proc.stdout.strip())
        return data
    except Exception:
        return []

def main():
    print("================================================================")
    print(" 🚀 AUTOMATED FILE UPLOADER FOR ZOSIMA.AI LAB 3 ASSESSMENT")
    print(" Candidate: Sai Nayan Mamilla | Host: Sais-MacBook-Pro.local")
    print("================================================================")

    for item in FILES_TO_UPLOAD:
        # If Q3 is already uploaded, we can still re-upload or ensure all are set
        upload_file(item["index"], item["filename"], item["path"])
        time.sleep(3.0) # Wait for Cloudflare R2 upload

    time.sleep(2.0)
    status = check_portal_status()
    print("\n==================================================")
    print(" 📋 CURRENT UPLOAD STATUS ON ZOSIMA.AI PORTAL:")
    print("==================================================")
    for i, s in enumerate(status, 1):
        icon = "✅" if s.get("uploaded") else "⏳"
        print(f" {icon} Item {i}: {s.get('name')} -> {'Uploaded' if s.get('uploaded') else 'Pending'}")
    print("==================================================")

if __name__ == "__main__":
    main()
