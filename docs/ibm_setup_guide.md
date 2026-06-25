# IBM watsonx.ai Setup Guide

This guide explains how to set up IBM watsonx.ai credentials for the World Cup Fan Intelligence Hub project.

## Prerequisites

- IBM Cloud account (free tier available)
- Python 3.8 or higher
- `ibm-watsonx-ai` package installed

## Step 1: Create IBM Cloud Account

1. Go to [IBM Cloud](https://cloud.ibm.com/registration)
2. Sign up for a free account
3. Verify your email address

## Step 2: Create watsonx.ai Project

1. Log in to [IBM Cloud](https://cloud.ibm.com)
2. Navigate to **watsonx.ai** service
3. Click **Create Project**
4. Name your project (e.g., "Football Fan Hub")
5. Note down your **Project ID** (you'll need this later)

## Step 3: Generate API Key

1. In IBM Cloud, click on **Manage** → **Access (IAM)**
2. Click **API keys** in the left sidebar
3. Click **Create an IBM Cloud API key**
4. Give it a name (e.g., "Football Hub API Key")
5. Click **Create**
6. **Important:** Copy and save the API key immediately (you won't be able to see it again)

## Step 4: Set Environment Variables

### Option A: Using .env file (Recommended for Development)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   IBM_CLOUD_API_KEY=your_api_key_here
   IBM_WATSONX_PROJECT_ID=your_project_id_here
   ```

3. The application will automatically load these variables

### Option B: System Environment Variables

**Windows (PowerShell):**
```powershell
$env:IBM_CLOUD_API_KEY="your_api_key_here"
$env:IBM_WATSONX_PROJECT_ID="your_project_id_here"
```

**Windows (Command Prompt):**
```cmd
set IBM_CLOUD_API_KEY=your_api_key_here
set IBM_WATSONX_PROJECT_ID=your_project_id_here
```

**Linux/Mac:**
```bash
export IBM_CLOUD_API_KEY="your_api_key_here"
export IBM_WATSONX_PROJECT_ID="your_project_id_here"
```

### Option C: Streamlit Secrets (For Deployment)

1. Create `.streamlit/secrets.toml`:
   ```toml
   IBM_CLOUD_API_KEY = "your_api_key_here"
   IBM_WATSONX_PROJECT_ID = "your_project_id_here"
   ```

2. When deploying to Streamlit Cloud, add these in the app settings

## Step 5: Install Required Package

```bash
pip install ibm-watsonx-ai
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Step 6: Test the Integration

Run the test script:
```bash
python src/ibm_granite_integration.py
```

You should see:
```
Initialization Status: [OK] Success
```

If you see `[FALLBACK] Using Fallback Mode`, check your credentials.

## Troubleshooting

### Error: "IBM credentials not found"
- Verify your `.env` file exists and contains the correct keys
- Check that environment variables are set correctly
- Ensure you're running the script from the project root directory

### Error: "Invalid API key"
- Verify you copied the entire API key
- Check for extra spaces or quotes
- Generate a new API key if needed

### Error: "Project not found"
- Verify your Project ID is correct
- Ensure the project exists in your IBM Cloud account
- Check that you have access to the project

### Error: "Package not installed"
- Run: `pip install ibm-watsonx-ai`
- Verify installation: `pip show ibm-watsonx-ai`

## IBM Granite Model Information

**Model ID:** `ibm/granite-13b-chat-v2`

**Capabilities:**
- Natural language generation
- Conversational AI
- Text explanation and summarization
- Factual and analytical content

**Parameters Used:**
- Max tokens: 200
- Temperature: 0.7 (balanced creativity)
- Top-p: 0.9 (nucleus sampling)
- Repetition penalty: 1.1 (reduce repetition)

## Free Tier Limits

IBM watsonx.ai free tier includes:
- Limited API calls per month
- Access to Granite models
- Suitable for development and testing

For production use, consider upgrading to a paid plan.

## Security Best Practices

1. **Never commit credentials to Git**
   - `.env` is in `.gitignore`
   - Use `.env.example` as a template

2. **Rotate API keys regularly**
   - Generate new keys every 90 days
   - Delete old keys after rotation

3. **Use separate keys for dev/prod**
   - Different keys for development and production
   - Easier to track usage and revoke if needed

4. **Limit key permissions**
   - Only grant necessary permissions
   - Use service-specific keys when possible

## Additional Resources

- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [IBM Granite Models](https://www.ibm.com/granite)
- [Python SDK Documentation](https://ibm.github.io/watsonx-ai-python-sdk/)
- [IBM Cloud API Keys](https://cloud.ibm.com/docs/account?topic=account-userapikey)

## Support

For issues with IBM watsonx.ai:
- [IBM Cloud Support](https://cloud.ibm.com/unifiedsupport/supportcenter)
- [Community Forums](https://community.ibm.com/community/user/watsonai/home)

For project-specific issues:
- Check the project README
- Review the troubleshooting section above
- Contact the project maintainer