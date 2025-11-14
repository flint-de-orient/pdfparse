@echo off
echo 🚀 Deploying PDF Parser to Vercel...

echo.
echo Step 1: Installing Vercel CLI...
npm install -g vercel

echo.
echo Step 2: Logging into Vercel...
vercel login

echo.
echo Step 3: Deploying project...
vercel --prod

echo.
echo ✅ Deployment complete!
echo Your app should be available at the URL shown above.

pause