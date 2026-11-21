@echo off
rem run_pipeline.bat - MFA Forced Alignment Pipeline Runner for Windows
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "BASE_DIR=%SCRIPT_DIR%.."
set "CORPUS_DIR=%BASE_DIR%\corpus_normalized"
set "DICT_DIR=%BASE_DIR%\dict"
set "OUTPUT_DIR=%BASE_DIR%\textgrid"

set "STOCK_DICT=%DICT_DIR%\english_us_arpa.dict"
set "CUSTOM_DICT=%DICT_DIR%\custom_us_arpa.dict"
set "ACOUSTIC_MODEL=english_us_arpa"

if not exist "%OUTPUT_DIR%\config_A" mkdir "%OUTPUT_DIR%\config_A"
if not exist "%OUTPUT_DIR%\config_B" mkdir "%OUTPUT_DIR%\config_B"
if not exist "%OUTPUT_DIR%\config_D" mkdir "%OUTPUT_DIR%\config_D"

echo ======================================================================
echo Assignment 2a: Montreal Forced Aligner Pipeline Execution
echo ======================================================================

rem Step 1: Preprocessing & Dictionary
python "%SCRIPT_DIR%prepare_corpus.py"
python "%SCRIPT_DIR%build_dictionary.py"

rem Check MFA runner command
where mfa >nul 2>nul
if %errorlevel% equ 0 (
    set "MFA_RUN=mfa"
) else (
    set "MFA_RUN=conda run -n mfa mfa"
)

rem Step 2: Config A - Baseline Stock Dictionary
echo.
echo [*] Running Config A: Stock english_us_arpa dictionary...
call %MFA_RUN% align "%CORPUS_DIR%" "%STOCK_DICT%" "%ACOUSTIC_MODEL%" "%OUTPUT_DIR%\config_A" --clean --overwrite

rem Step 3: Config B - Custom Curated Dictionary
echo.
echo [*] Running Config B: Custom dictionary (resolving OOVs)...
call %MFA_RUN% align "%CORPUS_DIR%" "%CUSTOM_DICT%" "%ACOUSTIC_MODEL%" "%OUTPUT_DIR%\config_B" --clean --overwrite

rem Step 4: Config D - Wide Beam Decoding
echo.
echo [*] Running Config D: Custom dictionary with Wide Beam...
call %MFA_RUN% align "%CORPUS_DIR%" "%CUSTOM_DICT%" "%ACOUSTIC_MODEL%" "%OUTPUT_DIR%\config_D" --beam 100 --retry_beam 400 --clean --overwrite

rem Step 5: Copy primary outputs
copy "%OUTPUT_DIR%\config_B\*.TextGrid" "%OUTPUT_DIR%\" >nul

echo.
echo ======================================================================
echo Pipeline execution complete. Outputs saved in: %OUTPUT_DIR%
echo ======================================================================
