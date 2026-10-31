# 02: FTX withdrawal scam

Sample: sample-10050.eml from [phishing_pot](https://github.com/rf-peixoto/phishing_pot)
Received: 2023-09-07 15:17 UTC

Verdict: phishing. Pretends to be FTX saying you can withdraw your crypto now. FTX went bankrupt in 2022, so a lot of people were waiting for an email like this. It passes SPF, DKIM and DMARC.

## Headers

```
From:        FTXinsurance <noreplye@promotix.com>
Return-Path: ...@amazonses.com
Subject:     Announcement : Withdraw Process is Authorized Now !

spf=pass   (sender IP 54.240.9.14, smtp.mailfrom=amazonses.com)
dkim=pass  header.d=promotix.com
dmarc=pass header.from=promotix.com
```

It was sent through Amazon SES, which is a real email sending service. SPF passed because the Return-Path is amazonses.com and that IP is Amazon's. DKIM passed for promotix.com, which matches the From address, so DMARC passed too.

The problem is promotix.com has nothing to do with FTX. I looked up its DNS records. The SPF allows Google, Amazon SES and HubSpot, and the DMARC policy is p=none. The domain is from 2002, so it's probably a real company's account or domain that got abused rather than something the attacker registered.

The only part that mentions FTX is the display name, "FTXinsurance". Also the address is noreplye@ instead of noreply@.

## Body

> "You have been identified as an eligible client to begin withdrawing digital assets from your FTX account... You can now withdraw to an external ERC-20 wallet..."

It has one button and an image attachment called thumbnailcpp.png (8.8 KB), which is just a logo.
SHA256: 5b9dc743098192649becd4f5fdd612d23772d1c24ffb824773a32048db33e8e9

## Link

```
hxxp://www.kif.re[.]kr/kif2///publication/viewer.aspx?controlno=229274&returnurl=hxxp://taurus-online[.]ch/wp/pf/
```

The link starts on kif.re.kr, which is a real Korean institute's website, so if you just look at the domain it seems fine. But at the end there's returnurl= pointing to taurus-online.ch. The site sends you to whatever returnurl is set to, so it's an open redirect. The real page is taurus-online.ch/wp/pf/, and /wp/ makes me think it's a hacked WordPress site hosting the fake FTX page.

## IOCs

```
promotix[.]com                              sender domain (probably abused)
hxxp://www.kif.re[.]kr/...returnurl=        open redirect on a real site
taurus-online[.]ch/wp/pf/                   actual phishing page
54.240.9.14                                 Amazon SES (don't block)
5b9dc743098192649becd4f5fdd612d23772d1c24ffb824773a32048db33e8e9   thumbnailcpp.png
```

## MITRE ATT&CK
- T1566.002 Phishing: Spearphishing Link
- T1036 Masquerading

## Response
- Block taurus-online.ch. Not kif.re.kr since that's a real site.
- Add an email filter for links with kif.re.kr and returnurl= in them, since they could reuse the redirect with a different destination
- Search mail logs for promotix.com and remove the emails
- If someone clicked, check whether they entered a wallet or login info
