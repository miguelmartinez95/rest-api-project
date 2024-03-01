"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be imported by
app and the logout resource so that tokens can be added to the blocklist when the
user logs out.
"""

BLOCKLIST = set()

#BETTER A DATABASE. SETS ARE RESET EACH TIME THE APP IS RUN. THE UISER BLOCKED WILL BE FORGOTTEN