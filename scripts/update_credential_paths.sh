#!/bin/bash
# Update all scripts to use secure credential paths in ~/.secrets/

REPO="/home/wrenn/clawd"
SECRETS="/home/wrenn/.secrets"

echo "🔒 Updating all scripts to use secure credential paths..."

# Update Python scripts
find "$REPO/scripts" -name "*.py" -type f -exec sed -i \
  -e "s|/home/wrenn/.secrets/stripe.json|$SECRETS/stripe.json|g" \
  -e "s|/home/wrenn/.secrets/xai.json|$SECRETS/xai.json|g" \
  -e "s|/home/wrenn/clawd/gmail-credentials.json|$SECRETS/gmail.json|g" \
  -e "s|/home/wrenn/clawd/gmail_credentials.txt|$SECRETS/gmail.txt|g" \
  -e "s|/home/wrenn/clawd/google-oauth-credentials.json|$SECRETS/google-oauth.json|g" \
  -e "s|/home/wrenn/clawd/google-calendar-token.json|$SECRETS/google-calendar.json|g" \
  -e "s|/home/wrenn/clawd/x-credentials.json|$SECRETS/x-twitter.json|g" \
  -e "s|/home/wrenn/clawd/brave-credentials.json|$SECRETS/brave.json|g" \
  -e "s|/home/wrenn/clawd/posthog-credentials.json|$SECRETS/posthog.json|g" \
  -e "s|/home/wrenn/clawd/notion-credentials.json|$SECRETS/notion.json|g" \
  {} \;

# Update bash scripts
find "$REPO/scripts" -name "*.sh" -type f -exec sed -i \
  -e "s|/home/wrenn/.secrets/xai.json|$SECRETS/xai.json|g" \
  -e "s|/home/wrenn/.secrets/stripe.json|$SECRETS/stripe.json|g" \
  {} \;

# Update config files
find "$REPO" -maxdepth 2 -name "*.env" -o -name "config.*" | while read f; do
  if [ -f "$f" ]; then
    sed -i -e "s|/home/wrenn/clawd/.*-credentials.json|$SECRETS/|g" "$f"
  fi
done

echo "✅ All scripts updated to use $SECRETS/"
echo ""
echo "Next steps:"
echo "1. Get new API keys from services"
echo "2. Create files in $SECRETS/ (see SETUP_INSTRUCTIONS.md)"
echo "3. Test each integration"
