# Streamlit Secrets Setup Guide

## Local Development

1. **Create the secrets file**: `.streamlit/secrets.toml` (already created)
2. **Fill in your actual values**: Replace the placeholder values with your real credentials
3. **Test your app**: Run `streamlit run app.py` to test locally

## Required Secrets

Based on your applications, you need to configure these secrets:

### Google Sheets URLs
- `mentee_response_sheet_url`
- `mentee_response_stage2_sheet_url` 
- `mentee_matching_sheet_url`
- `mentor_matching_result_sheet_url`
- `mentor_matching_result_both_stage_sheet_url`
- `mentee_matching_stage2_sheet_url`
- `mentee_sheet_url`
- `mentor_sheet_url`
- `mentee_data`
- `mentor_data`
- `mentor_matched_url`
- `mentee_matched_url`

### Auth0 Configuration
- `auth0_domain`
- `auth0_client_id`
- `auth0_client_secret`
- `auth0_redirect_uri`
- `auth0_audience` (optional)

## How to Get Google Sheets URLs

1. Open your Google Sheet
2. Click "Share" → "Get link"
3. Make sure it's set to "Anyone with the link can view"
4. Copy the URL (it should look like: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit#gid=GID_NUMBER`)

## Deployment on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. In the "Advanced settings", add your secrets in the "Secrets" section
4. Use the same TOML format as your local secrets file

## Security Notes

- ✅ Never commit `.streamlit/secrets.toml` to version control
- ✅ Use environment-specific values (different for dev/prod)
- ✅ Regularly rotate sensitive credentials
- ✅ Use least-privilege access for Google Sheets (view-only when possible)

## Testing Your Setup

Run this command to test if secrets are loaded correctly:

```bash
streamlit run app.py
```

If you see any "KeyError" messages, it means a secret is missing or misnamed.