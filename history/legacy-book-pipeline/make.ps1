# Regenerate the whole book, then copy deliverables into the session-state folder.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "[1/5] Master problem index..." -ForegroundColor Cyan
python src\gen_index.py

Write-Host "[2/5] Editable DSA_MASTER_REFERENCE2.md..." -ForegroundColor Cyan
python src\gen_master_md.py

Write-Host "[3/5] Building paged HTML..." -ForegroundColor Cyan
python src\build.py

Write-Host "[4/5] Rendering PDF (paged.js)..." -ForegroundColor Cyan
npx pagedjs-cli build\book.html -o "DSA_MASTER_REFERENCE2.pdf"

python -c "import fitz; print('PAGES', fitz.open('DSA_MASTER_REFERENCE2.pdf').page_count)"

Write-Host "[5/5] Copying deliverables into session-state (persistent)..." -ForegroundColor Cyan
$dest = "C:\Users\absinghal\.copilot\session-state\d63f7455-acff-41b9-9f54-82ae93f02967\files"
if (Test-Path $dest) {
  Copy-Item "DSA_MASTER_REFERENCE2.pdf" $dest -Force
  Copy-Item "DSA_MASTER_REFERENCE2.md"  $dest -Force
  Write-Host "Copied to $dest" -ForegroundColor Green
}
Write-Host "Done. Output: DSA_MASTER_REFERENCE2.pdf" -ForegroundColor Green
