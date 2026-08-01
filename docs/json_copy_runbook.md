# JSON Dataset Copy Runbook (WSL + Windows Drive)

## When to use this
Use this when copying many small MOF JSON files from a Windows-mounted path (for example, `/mnt/d/...`) into local Linux storage for Phase 2 processing.

This is mainly a speed and stability optimization for repeated preprocessing/feature extraction.

## Source and destination used in this project
- Source: `/mnt/d/MOf/hMOF-10 1039 C2EE23201D-CarbonDioxide-mofdb-version_dc8a0295db`
- Destination: `~/MOF_project/data/raw/hmof_json_local`

## Important command note
Do not use `sync` for copying. `sync` only flushes filesystem buffers.

Use `rsync` or `cp`.

## Recommended copy command
```bash
mkdir -p "$HOME/MOF_project/data/raw/hmof_json_local"
cp -a "/mnt/d/MOf/hMOF-10 1039 C2EE23201D-CarbonDioxide-mofdb-version_dc8a0295db/." \
  "$HOME/MOF_project/data/raw/hmof_json_local/"
```

## Alternative resumable command
If a copy is interrupted, resume safely with `rsync`:

```bash
rsync -a --partial \
  "/mnt/d/MOf/hMOF-10 1039 C2EE23201D-CarbonDioxide-mofdb-version_dc8a0295db/" \
  "$HOME/MOF_project/data/raw/hmof_json_local/"
```

## Progress checks
Check destination growth while copy is running:

```bash
dest="$HOME/MOF_project/data/raw/hmof_json_local"
find "$dest" -type f | wc -l
du -sb "$dest"
```

Check running copy process:

```bash
ps -eo pid=,args= | grep '[c]p' | grep -F '/mnt/d/MOf/hMOF-10 1039 C2EE23201D-CarbonDioxide-mofdb-version_dc8a0295db'
```

## Final verification (required)
Compare source and destination file counts:

```bash
src='/mnt/d/MOf/hMOF-10 1039 C2EE23201D-CarbonDioxide-mofdb-version_dc8a0295db'
dest="$HOME/MOF_project/data/raw/hmof_json_local"

echo "SOURCE files:" && find "$src" -type f | wc -l
echo "DEST files:" && find "$dest" -type f | wc -l
```

Counts should match before starting full Phase 2 processing.

## Troubleshooting
- `rsync` exit code 20 usually means interrupted by signal (for example Ctrl+C).
- If transfer appears stuck with no file growth for a long time, stop it and restart with the `cp -a` command above.
- Many small files from `/mnt/d` can be slower than expected due to per-file overhead.

## Why this matters for this project
`src/preprocess.py` and Phase 2 chemistry-feature steps depend on fast access to local JSON files. Keeping a local copy reduces repeated `/mnt/d` overhead in WSL.
