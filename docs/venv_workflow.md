# Complete Workflow: Setting Up a Python Environment for Any Project

---

## Step 1 — Open Your Project in VS Code

```bash
cd /home/susan/mof-co2-adsorption
code .
```

---

## Step 2 — Create Virtual Environment via VS Code

Open the Command Palette:
- Press `Ctrl+Shift+P`
- Type: `Python: Create Environment`
- Select **Venv**
- Select **Python 3.12.3** as the base interpreter
- Wait for VS Code to create `.venv` inside your project

---

## Step 3 — Verify the Environment Was Created

```bash
ls .venv/bin/
# Expected output: activate  pip  pip3  python  python3
```

---

## Step 4 — Activate It in the Terminal

```bash
source /home/susan/mof-co2-adsorption/.venv/bin/activate
```

Your prompt should show:
```
(.venv) susan@Susan:~/mof-co2-adsorption$
```

Verify you are inside the venv:
```bash
which python
# Expected: /home/susan/mof-co2-adsorption/.venv/bin/python

which pip
# Expected: /home/susan/mof-co2-adsorption/.venv/bin/pip
```

---

## Step 5 — Upgrade pip Inside the venv

```bash
pip install --upgrade pip
```

---

## Step 6 — Install All Required Packages

```bash
pip install pytest pandas numpy matplotlib seaborn scikit-learn jupyter
```

---

## Step 7 — Save Your Dependencies to a File

```bash
pip freeze > requirements.txt
```

Anyone can recreate your environment using:
```bash
pip install -r requirements.txt
```

---

## Step 8 — Tell VS Code to Use This Interpreter

- Press `Ctrl+Shift+P`
- Type: `Python: Select Interpreter`
- Choose: `Python 3.12.3 ('.venv': venv)`

---

## Step 9 — Verify Everything Works

```bash
python --version
# Expected: Python 3.12.3

pip --version
# Expected: pip xx.x.x from .venv/...

pytest --version
# Expected: pytest 8.x.x

python -c "import pandas, numpy, sklearn; print('All packages OK')"
# Expected: All packages OK
```

---

## Every Time You Open a New Terminal

```bash
source /home/susan/mof-co2-adsorption/.venv/bin/activate
```

---

## If You Need to Delete and Recreate the venv

```bash
# Delete broken venv
rm -rf /home/susan/mof-co2-adsorption/.venv

# Install required system package
sudo apt install python3-full python3-venv

# Recreate
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Reinstall all packages
pip install -r requirements.txt
```

---

## Summary Checklist

| Step | Command | Purpose |
|---|---|---|
| Create venv | `Ctrl+Shift+P` → Create Environment | Isolated Python |
| Activate | `source .venv/bin/activate` | Use venv pip and python |
| Upgrade pip | `pip install --upgrade pip` | Latest pip version |
| Install packages | `pip install pandas numpy scikit-learn` | Project dependencies |
| Save dependencies | `pip freeze > requirements.txt` | Reproducibility |
| Select interpreter | `Ctrl+Shift+P` → Select Interpreter | VS Code uses venv |
| Verify | `python -c "import pandas; print('OK')"` | Confirm setup works |

---

## Project Folder Structure After Setup

```
mof-co2-adsorption/
├── .venv/                  ← virtual environment (never edit manually)
├── data/
│   └── processed/
├── docs/
│   └── venv_workflow.md    ← this file
├── notebook/
│   └── modeling/
├── tests/
│   └── test_model.py
├── requirements.txt        ← package list
└── README.md
```

---

## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `externally-managed-environment` | Using system pip | Activate `.venv` first |
| `pip: cannot execute` | Broken venv | Delete and recreate venv |
| `which python` → not found | venv not activated | Run `source .venv/bin/activate` |
| `ModuleNotFoundError` | Package not installed in venv | Run `pip install <package>` |

---

> **Golden Rule:** Never use `sudo pip` or system `pip`.  
> Always activate `.venv` first.  
> One project = one `.venv`.