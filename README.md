# Phishing Email Analysis

Analysis of real phishing emails, done the way I'd handle a user-reported email in a SOC. For each one I went through the headers, checked SPF/DKIM/DMARC, figured out where it actually came from, pulled out the links and attachments without opening them, and wrote down what I'd block.

The emails are from [phishing_pot](https://github.com/rf-peixoto/phishing_pot), a public collection of phishing emails caught by honeypots (CC BY-NC 4.0). I downloaded a random 39 of them and picked 4 that were different from each other. I didn't include the raw .eml files here.

## Reports

1. [Fake cloud storage warning](reports/01-fake-cloud-storage.md): sent from a throwaway Microsoft 365 account through Google. 10 of the 39 emails I downloaded linked to the same domain.
2. [FTX withdrawal scam](reports/02-ftx-withdrawal.md): passes SPF, DKIM and DMARC but it's still phishing
3. [Harbor Freight rewards](reports/03-harbor-freight-rewards.md): just two images with TinyURL links, sent through a Google Group
4. [Fake antivirus renewal](reports/04-antivirus-renewal.md): a bunch of unrelated domains in one email and a Reply-To that doesn't match the sender

## Notes

Before this I assumed if an email passed SPF, DKIM and DMARC it was probably fine. Two of these four passed all three. Those checks only tell you the domain allowed the email to be sent, not that the domain belongs to who the email says it's from.

It's also worth checking what domain DKIM actually signed for. In #1 and #4 it passed, but for a domain that had nothing to do with the sender.

Blocking the sender wouldn't have done much for most of these since the addresses are random and change every time. The link domains were more useful to block.

## Files

- `analysis-checklist.md` - what I go through for each email
- `parse_eml.py` - small Python script that prints the headers, auth results, links and attachment hashes from an .eml file so I didn't have to scroll through the raw file. It hashes attachments without saving or opening them.

I didn't click any links or open any attachments. URLs in the reports are defanged (hxxp, [.]).
