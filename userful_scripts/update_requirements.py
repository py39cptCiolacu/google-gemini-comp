import subprocess

# Nu merge deocamdata
 
UPDATE_REQ_COMMAND = """
.\\google_gemini_comp\\Scripts\\activate
pip freeze > .\requirements.txt
"""

def update_requirements() -> None:
    try:
        subprocess.run(UPDATE_REQ_COMMAND, shell=True, check=True)
        print("Done")
    except subprocess.CalledProcessError as e:
        print(f"Eroarea a fost: {e}")

if __name__ == "__main__":
    update_requirements()
