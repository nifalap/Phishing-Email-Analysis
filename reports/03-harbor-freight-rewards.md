# 03: Harbor Freight rewards

Sample: sample-10529.eml from [phishing_pot](https://github.com/rf-peixoto/phishing_pot)
Received: 2023-06-29 17:25 UTC

Verdict: phishing. Fake Harbor Freight reward. There's no text in the email, only two images that link to TinyURL. It was sent out through a Google Group.

## Headers

```
From:        #Harbor_Freight_Rewards# <farahatsanae@gmail.com>
Return-Path: xdtcfjhvtrsdfgcgbnbxgvcbnn+bncBCF...@bravo67.click
To:          ajnxsxasjxsnxzxasascdcvdv@buffalopin.click
Subject:     _Confirmation-48628*Rlk2_
List-Id:     <xdtcfjhvtrsdfgcgbnbxgvcbnn.bravo67.click>
X-Google-Group-Id: 641582657633

spf=none   smtp.mailfrom=bravo67.click
dkim=pass  header.d=bravo67-click.20221208.gappssmtp.com
dmarc=fail header.from=gmail.com
```

The display name says Harbor Freight but it's from a random Gmail address.

The To address isn't the person who got it, it's another junk address on buffalopin.click. The List-Id, X-Google-Group-Id and the +bnc in the Return-Path mean it went through a Google Group on bravo67.click. So they sent one email from Gmail to the group, and the group sent it out to everyone on it.

The ARC headers show the original email from Gmail passed SPF and DKIM. After the group resent it, the From was still gmail.com but it was coming from bravo67.click, so DMARC failed. Gmail's policy in the header was p=none so it got delivered anyway.

The subject is just random characters, probably to get past spam filters looking for keywords.

## Body

This is pretty much the whole email:

```html
<a href="hxxps://tinyurl[.]com/4vffukd9"><img src="hxxps://i.imgur[.]com/7bH1Wde.png"></a>
<a href="hxxps://tinyurl[.]com/yhxs5ck5"><img src="hxxps://i.imgur[.]com/YDqkJJs.png"></a>
```

There's no text to scan. Whatever the email says is inside the images on Imgur, and the links are behind TinyURL so you can't see where they go. I didn't expand them.

## IOCs

```
farahatsanae@gmail[.]com             sender
bravo67[.]click                      Google Group domain
buffalopin[.]click                   To domain
hxxps://tinyurl[.]com/4vffukd9
hxxps://tinyurl[.]com/yhxs5ck5
```

## MITRE ATT&CK
- T1566.002 Phishing: Spearphishing Link
- T1036 Masquerading

## Response
- Block the two TinyURL links and both .click domains
- Report the Gmail account and the TinyURL links for abuse
- Search mail logs for bravo67.click in the Return-Path or List-Id. The Gmail sender will probably change but the group might not.
- An email that's only images and short links from a Gmail address is almost never legit, could be a filter rule
