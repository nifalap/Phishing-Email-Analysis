# Checklist

What I go through for each email.

Sender
- Does the display name match the actual email address?
- Are Return-Path and Reply-To the same domain as From?
- Is it from a free email provider or a weird domain (random letters, onmicrosoft.com, .click etc)?

Authentication-Results header
- SPF pass/fail, and for what domain
- DKIM pass/fail, and what domain signed it (header.d=)
- DMARC result and policy. p=none means nothing gets blocked even if it fails.

Received headers
- Read from the bottom up, the bottom one is closest to where it was sent from
- Does the path make sense for who it says it's from?

Body
- Urgent wording like "final notice" or "action required"
- Generic greeting like "Dear user"
- Hidden text (display:none) or a body that's only images

Links (don't click)
- Shorteners like tinyurl or bit.ly
- Real sites with a redirect in the URL (returnurl=, url=, redirect=)
- Pages hosted on cloud storage like storage.googleapis.com
- Long random IDs in the link, which usually means they're tracking who clicked

Attachments (don't open)
- Get the SHA256 and look it up
- Be careful with .html, .zip, .iso, .js and double extensions

After that
- Phishing, spam or legit?
- What to block. Link domains first. Don't block shared mail servers like Google or Amazon SES.
- Search mail logs for other copies
- Check proxy logs to see if anyone clicked
