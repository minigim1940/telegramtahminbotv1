@echo off
echo ============================================
echo  Telegram Tahmin Bot - Render.com Deploy
echo ============================================
echo.

REM Git kontrolu
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [HATA] Git yuklu degil!
    echo Git indirin: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Git repository baslat...
if not exist .git (
    git init
    echo Git repository baslatildi.
) else (
    echo Git repository mevcut.
)

echo.
echo [2/5] GitHub kullanici adi girin:
set /p GITHUB_USER="GitHub kullanici adiniz: "

echo.
echo [3/5] Repository adi:
set /p REPO_NAME="Repository adi (varsayilan: telegram-tahmin-bot): "
if "%REPO_NAME%"=="" set REPO_NAME=telegram-tahmin-bot

echo.
echo [4/5] Dosyalari ekle ve commit yap...
git add .
git commit -m "Initial commit - Telegram Tahmin Bot"

echo.
echo [5/5] GitHub'a push et...
echo.
echo ONCE GitHub'da yeni repository olusturun:
echo https://github.com/new
echo.
echo Repository adi: %REPO_NAME%
echo Private yapmayi unutmayin!
echo.
pause

git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
git push -u origin main

echo.
echo ============================================
echo  TAMAMLANDI!
echo ============================================
echo.
echo Simdi Render.com'a gidin:
echo https://dashboard.render.com
echo.
echo 1. "New +" tiklayin
echo 2. "Background Worker" secin
echo 3. Repository'nizi baglayın
echo 4. Environment Variables ekleyin:
echo    - TELEGRAM_BOT_TOKEN
echo    - ADMIN_IDS (opsiyonel)
echo.
echo Detayli talimatlar: RENDER_DEPLOYMENT.md
echo ============================================
pause
