# Fyers-Auto


This script is intended to automate the opening range breakout trades over a selected range of stocks. As stock selection rules for long and short trades are completely different, genrates different sets of stocks.

Steps to use:
1. Install the required libraries by using
```bash
pip install -r requirements.txt
```
2. Creat an app by going to `https://myapi.fyers.in/create-ApiV2-app`
3. Provide `http://localhost` as redirect uri as during auth code generation this uri will be redirected to. As auth code should be secret, always use the uri which is in your control.
4. After creation of the app, note the app id and the secret key.
5. Enter therequired details into `creds.py`. 
6. Enable 2FA in `https://myaccount.fyers.in/`.
7. Put stocks symbol in long and short list in `master_data.py`. Eg: 'SBIN', 'INFY', 'NTPC', etc.
8. The code is designed to take trade from 9.45 am. That means when 1st 30 minute range breaks, it will go long or short.
9. Code won't take any trade after 1 pm and all existing positions will be closed after 3 pm.
10. Happy Hunting. :)