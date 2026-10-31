# 01: Fake cloud storage warning

Sample: sample-10398.eml from [phishing_pot](https://github.com/rf-peixoto/phishing_pot)
Received: 2026-05-10 14:57 UTC

Verdict: phishing. Says your cloud storage is full and your photos will be deleted. It's part of a larger campaign.

## Headers

```
From:        Storage Notification <ocean.davis@sbdsdbdcelebsnetworthnet.onmicrosoft.com>
Return-Path: ocean.davis@sbdsdbdcelebsnetworthnet.onmicrosoft.com
Subject:     Action Required: Your photos and videos will be lost
Message-ID:  <...@mail.gmail.com>

spf=fail (sender IP is 209.85.210.176)
dkim=pass header.d=sbdsdbdcelebsnetworthnet-onmicrosoft-com.20251104.gappssmtp.com
dmarc=none
```

The sender is an onmicrosoft.com address. Every new Microsoft 365 tenant gets one of those by default, so anyone can make one, and the name is just random letters.

It wasn't actually sent from Microsoft though. The Received headers show it came from a Google mail server (mail-pf1-f176.google.com) and before that the Gmail API, and the Message-ID ends in @mail.gmail.com. That's why SPF failed, since onmicrosoft.com only allows Microsoft's servers.

DKIM passed, but the signing domain is a Google Workspace domain (gappssmtp.com), not the sender's domain, so it doesn't prove anything. DMARC was none, so the failed SPF didn't get it blocked.

The display name is just "Storage Notification" and never names a company, so it could fool someone using iCloud, Google Drive or OneDrive.

## Body

What you see is a "Your Cloud Storage Is Full" warning with a Continue button.

In the HTML there's also a div with display:none that has around 213,000 characters of random letters and numbers in it. You can't see it in the email. I'm pretty sure it's there to throw off spam filters that look at the text.

## Links

```
hxxps://woondsplay[.]com/4yzSAd20558...     Continue button
hxxp://woondsplay[.]com/rd/5uTSwV20558...   redirect
hxxps://woondsplay[.]com/track/3gqEBW...    tracking pixel
hxxps://i.imgur[.]com/l5706eG.png           image
```

Each link has a long ID in it, probably so they know which person clicked.

## Other emails with the same domain

I searched the other 38 emails I downloaded for woondsplay.com and it was in 10 of them. They were all different kinds of scams (casino bonuses, "your reward is available", a bank check) with different senders. 8 of the 10 were from random onmicrosoft.com addresses sent through Google with SPF failing, same as this one.

So the sender changes every time, but they all point to the same link domain. Blocking woondsplay.com would catch all of them.

## IOCs

```
woondsplay[.]com                                   link domain
sbdsdbdcelebsnetworthnet[.]onmicrosoft[.]com       sender domain
209.85.210.176                                     Google mail server (don't block)
```

## MITRE ATT&CK
- T1566.002 Phishing: Spearphishing Link
- T1585.002 Establish Accounts: Email Accounts

## Response
- Block woondsplay.com on the proxy and email gateway
- Search mail logs for that domain and remove the emails
- Check proxy logs for anyone who clicked
- Could also flag onmicrosoft.com senders that fail SPF. Real companies usually don't send from their default tenant domain.
