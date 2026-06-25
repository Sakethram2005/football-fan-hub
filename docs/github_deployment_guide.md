# 🚀 GitHub Deployment Guide

Complete guide to push your World Cup Fan Intelligence Hub to GitHub and prepare for submission.

---

## 📋 Pre-Deployment Checklist

### 1. Verify Local Repository Status

```bash
# Check current status
git status

# View commit history
git log --oneline

# Verify all files are committed
git diff
```

**Expected**: All changes should be committed, working directory clean.

### 2. Verify .gitignore is Working

```bash
# Check what files are being tracked
git ls-files

# Verify sensitive files are NOT tracked
git ls-files | grep -E "\.env$|__pycache__|\.pkl$"
```

**Important**: `.env` file should NOT appear in the list!

### 3. Test Application Locally

```bash
# Run tests
python tests/test_streamlit_app.py

# Start application
streamlit run app/main.py
```

**Expected**: All tests pass, application runs without errors.

---

## 🌐 Create GitHub Repository

### Option 1: GitHub Web Interface (Recommended for Beginners)

1. **Go to GitHub**: https://github.com/new
2. **Repository Details**:
   - **Name**: `football-fan-hub` or `world-cup-fan-intelligence-hub`
   - **Description**: "AI-powered football match predictions with IBM watsonx.ai - IBM SkillsBuild AI Builders Challenge 2026"
   - **Visibility**: ✅ **Public** (required for submission)
   - **Initialize**: ❌ Do NOT initialize with README (we already have one)
3. **Click**: "Create repository"

### Option 2: GitHub CLI

```bash
# Install GitHub CLI if not already installed
# Windows: winget install GitHub.cli
# Mac: brew install gh

# Login to GitHub
gh auth login

# Create repository
gh repo create football-fan-hub --public --description "AI-powered football match predictions with IBM watsonx.ai"
```

---

## 📤 Push to GitHub

### Step 1: Add Remote Repository

After creating the GitHub repository, you'll see a URL like:
`https://github.com/yourusername/football-fan-hub.git`

```bash
# Add remote (replace with your actual URL)
git remote add origin https://github.com/yourusername/football-fan-hub.git

# Verify remote was added
git remote -v
```

### Step 2: Push Your Code

```bash
# Push to main branch
git push -u origin master

# Or if your default branch is 'main'
git branch -M main
git push -u origin main
```

**Note**: You may be prompted for GitHub credentials. Use a Personal Access Token (PAT) instead of password.

### Step 3: Verify Upload

1. Go to your GitHub repository URL
2. Verify all files are present
3. Check that README.md displays correctly
4. Verify .env file is NOT visible (should be in .gitignore)

---

## 🔐 GitHub Personal Access Token (PAT)

If you need to create a PAT for authentication:

1. **Go to**: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Click**: "Generate new token (classic)"
3. **Settings**:
   - Note: "Football Fan Hub Deployment"
   - Expiration: 90 days
   - Scopes: ✅ `repo` (full control of private repositories)
4. **Generate** and **copy** the token (you won't see it again!)
5. **Use** the token as your password when pushing

---

## 📝 Update Repository Settings

### 1. Add Topics (Tags)

Go to your repository → About section → Settings icon

Add topics:
- `ibm-watsonx`
- `machine-learning`
- `streamlit`
- `football-analytics`
- `ai-predictions`
- `ibm-skillsbuild`
- `python`
- `data-science`

### 2. Set Repository Description

Update the description to:
> AI-powered football match predictions with IBM watsonx.ai explanations. Built for IBM SkillsBuild AI Builders Challenge 2026. Features ML predictions, team statistics, and head-to-head analysis.

### 3. Add Website Link

If you deploy to Streamlit Cloud (optional), add the URL here.

---

## 🎨 Enhance Repository Appearance

### 1. Add Social Preview Image

1. Go to repository Settings
2. Scroll to "Social preview"
3. Upload an image (1280x640px recommended)
4. Use a screenshot of your application or create a banner

### 2. Pin Repository

1. Go to your GitHub profile
2. Click "Customize your pins"
3. Select this repository to feature it

---

## 🚀 Optional: Deploy to Streamlit Cloud

### Why Deploy?

- Live demo accessible to judges
- No local setup required
- Professional presentation
- Free hosting for public repos

### Deployment Steps

1. **Go to**: https://streamlit.io/cloud
2. **Sign in** with GitHub
3. **New app** → Select your repository
4. **Settings**:
   - Branch: `main` or `master`
   - Main file path: `app/main.py`
   - Python version: 3.10+
5. **Advanced settings** → Add secrets:
   ```toml
   WATSONX_API_KEY = "your_api_key"
   WATSONX_PROJECT_ID = "your_project_id"
   WATSONX_URL = "https://eu-de.ml.cloud.ibm.com"
   ```
6. **Deploy**!

**Note**: The trained model (112 MB) might be too large for Streamlit Cloud free tier. Consider:
- Using Git LFS for large files
- Hosting model on cloud storage
- Training a smaller model for demo

---

## 📋 Final Repository Checklist

Before submission, verify your repository has:

- [ ] ✅ Public visibility
- [ ] ✅ Comprehensive README.md with:
  - [ ] Problem statement
  - [ ] Solution description
  - [ ] Technical architecture
  - [ ] Installation instructions
  - [ ] IBM watsonx.ai integration details
  - [ ] Screenshots or demo video link
- [ ] ✅ Complete source code
- [ ] ✅ requirements.txt with all dependencies
- [ ] ✅ .gitignore (no sensitive files)
- [ ] ✅ LICENSE file (MIT)
- [ ] ✅ Documentation in docs/ folder
- [ ] ✅ Test files
- [ ] ✅ Clear commit history
- [ ] ✅ Repository description and topics
- [ ] ✅ No .env file in repository
- [ ] ✅ All code properly commented

---

## 🔍 Verify Repository Quality

### Check README Rendering

1. View README.md on GitHub
2. Verify all markdown renders correctly
3. Check that images/badges display
4. Test all links work

### Check Code Quality

```bash
# Check for common issues
git log --all --full-history -- "*.env"  # Should return nothing

# Verify file sizes
git ls-files -z | xargs -0 du -h | sort -h | tail -20
```

### Test Clone

```bash
# Clone in a new directory to test
cd /tmp
git clone https://github.com/yourusername/football-fan-hub.git
cd football-fan-hub

# Verify it works
pip install -r requirements.txt
python tests/test_streamlit_app.py
```

---

## 📊 Repository Statistics

After pushing, your repository should show:

- **Languages**: Python (primary)
- **Size**: ~15-20 MB (without large model files)
- **Commits**: 6-8 commits
- **Files**: 30+ files
- **Folders**: Organized structure

---

## 🎯 Submission Preparation

### 1. Get Repository URL

Your public repository URL will be:
```
https://github.com/yourusername/football-fan-hub
```

### 2. Prepare Submission Materials

For IBM SkillsBuild submission, you'll need:

1. **GitHub Repository URL** ✅
2. **Demo Video Link** (YouTube/Vimeo)
3. **Project Description** (from README)
4. **Technologies Used**:
   - IBM watsonx.ai (Llama 3.3 70B)
   - Python 3.14
   - Streamlit
   - scikit-learn
   - pandas, numpy
   - Plotly

### 3. Create Submission Document

Create a file `SUBMISSION.md`:

```markdown
# IBM SkillsBuild AI Builders Challenge - June 2026
## World Cup Fan Intelligence Hub

**Participant**: [Your Name]
**Email**: [Your Email]
**Date**: June 25, 2026

### Project Links
- **GitHub Repository**: https://github.com/yourusername/football-fan-hub
- **Demo Video**: [YouTube Link]
- **Live Demo** (optional): [Streamlit Cloud Link]

### Project Summary
[Brief 2-3 sentence summary]

### IBM Technologies Used
- IBM watsonx.ai (Llama 3.3 70B model)
- IBM Watson Machine Learning

### Key Features
1. AI-powered match predictions
2. Plain-English explanations
3. Team statistics dashboard
4. Head-to-head analysis

### Dataset
49,329 international football matches (1872-2026)

### Model Performance
55% accuracy on 3-class prediction (Win/Draw/Loss)
```

---

## 🐛 Common Issues and Solutions

### Issue 1: Push Rejected (Large Files)

**Problem**: Model files too large for GitHub

**Solution**:
```bash
# Use Git LFS for large files
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git commit -m "Add Git LFS for model files"
git push
```

### Issue 2: Authentication Failed

**Problem**: Can't push to GitHub

**Solution**: Use Personal Access Token instead of password

### Issue 3: .env File Accidentally Committed

**Problem**: Sensitive data in repository

**Solution**:
```bash
# Remove from history
git rm --cached .env
git commit -m "Remove .env from tracking"
git push

# Then change your API keys immediately!
```

### Issue 4: README Not Displaying Correctly

**Problem**: Markdown formatting issues

**Solution**: Use GitHub's markdown preview or online tools to test

---

## ✅ Post-Deployment Checklist

After successful deployment:

- [ ] Repository is public and accessible
- [ ] README displays correctly with all sections
- [ ] No sensitive information visible
- [ ] All links in README work
- [ ] Code is well-organized and commented
- [ ] Tests pass when cloned fresh
- [ ] Demo video link added to README
- [ ] Repository URL ready for submission
- [ ] Submission document prepared

---

## 🎉 You're Ready!

Your project is now:
- ✅ Version controlled with Git
- ✅ Hosted on GitHub (public)
- ✅ Documented comprehensively
- ✅ Ready for submission
- ✅ Accessible to judges and community

**Next Steps**:
1. Record your demo video
2. Upload video to YouTube
3. Add video link to README
4. Submit to IBM SkillsBuild
5. Share with the community!

---

## 📞 Need Help?

- **GitHub Docs**: https://docs.github.com
- **Git Basics**: https://git-scm.com/doc
- **Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud
- **IBM watsonx.ai**: https://www.ibm.com/docs/en/watsonx-as-a-service

**Good luck with your submission! 🚀⚽**