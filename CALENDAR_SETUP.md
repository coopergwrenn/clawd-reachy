# Calendar OAuth Setup - One Time Only

Run this command on your local machine (not via Telegram):

```bash
cd /home/wrenn/clawd/scripts && ./setup_calendar_oauth.py
```

This will:
1. Open a browser window
2. Ask you to log in with coopergrantwrenn@gmail.com
3. Click "Allow" to grant calendar access
4. Save the token permanently

After this, morning reports will include your actual calendar events automatically.

---

**Alternative if that doesn't work:**

SSH into spark-7694 and run:
```bash
export DISPLAY=:0
cd /home/wrenn/clawd/scripts && ./setup_calendar_oauth.py
```

The OAuth needs a browser, which is why I can't do it automatically from Telegram.
