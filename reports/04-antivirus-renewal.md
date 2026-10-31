# 04: Fake antivirus renewal

Sample: sample-10519.eml from [phishing_pot](https://github.com/rf-peixoto/phishing_pot)
Received: 2026-04-28 15:26 UTC

Verdict: phishing. Fake "your antivirus is expiring" email. Like #2 it passes SPF, DKIM and DMARC.

## Headers

```
From:        Antivirus Total Protection <renewuxieqa@jillharrelsonphotography.com>
Return-Path: renewrmglhw@jillharrelsonphotography.com
Reply-To:    replyto@brendamurphyrealestate.com
To:          Undisclosed recipients:;
Subject:     Final Notice Protection Expires Today
Message-ID:  <swyohic.ggcgpo.ttcc@knjvbpxy.com>

spf=pass   (sender IP 20.127.99.54)
dkim=pass  header.d=gznp.themixtinsband.info
dmarc=pass header.from=jillharrelsonphotography.com
```

There are a lot of domains in this one and none of them are related:

- From / Return-Path: jillharrelsonphotography.com
- Reply-To: brendamurphyrealestate.com
- DKIM and sending server: gznp.themixtinsband.info (20.127.99.54)
- Message-ID: knjvbpxy.com

Nothing to do with antivirus. They look like small business domains that got hijacked or expired and were picked up by someone else. When I looked up the photography domain's DNS it didn't have an SPF record anymore.

DMARC passed because of SPF. The Return-Path and From are the same domain and SPF passed for it. The DKIM was for a different domain so it didn't count for DMARC.

The Reply-To is a different domain from the From, so if you reply it goes somewhere else. The sender addresses are random letters (renewuxieqa, renewrmglhw), and "Undisclosed recipients" means it was BCC'd to a lot of people.

## Body

Short. "Your Antivirus subscription has expired", a couple of images and a button. It never names a real antivirus company.

## Links

```
hxxps://storage.googleapis[.]com/aaprwwfxuqqpnxb/fmjuzgmwwm.html#S2EhCHp...
hxxp://klakmuf[.]com/5v69291mhIrDvnEOLQu0C8dV/...
hxxps://i.imgur[.]com/GKEsKEY.png
```

The button goes to an HTML file on Google Cloud Storage. Since it's a Google domain a lot of filters will let it through.

The part after the # doesn't get sent to the server, but JavaScript on the page can read it. My guess is they use it to pass a victim ID or the next redirect without it showing up in proxy logs.

klakmuf.com is the other link, probably unsubscribe or another redirect.

## IOCs

```
jillharrelsonphotography[.]com       From / Return-Path
brendamurphyrealestate[.]com         Reply-To
gznp.themixtinsband[.]info           sending server / DKIM
20.127.99.54                         sending IP
hxxps://storage.googleapis[.]com/aaprwwfxuqqpnxb/fmjuzgmwwm.html
klakmuf[.]com
```

## MITRE ATT&CK
- T1566.002 Phishing: Spearphishing Link
- T1036 Masquerading
- T1584.001 Compromise Infrastructure: Domains

## Response
- Block the exact Google Storage URL and klakmuf.com. Not all of storage.googleapis.com, that would break a lot of things.
- Report the bucket to Google
- Block the sending IP and themixtinsband.info on the email gateway
- Search mail logs for the Reply-To domain since it'll probably change less than the From
- Possible rule: Reply-To domain doesn't match From, plus words like renewal, expires or invoice
