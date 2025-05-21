@echo off
echo Initializing Git repository...

git init
git remote add origin https://github.com/mahmoud0357/ChatBot.git
git add .
git commit -m "Initial commit for QueryMancer ChatBot"
git branch -M main
git push -u origin main

echo ✅ Project Deployed to GitHub Successfully!
pause
