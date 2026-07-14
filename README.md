# Wimsatt Welder Repair — website

A single-page website that turns visitors into a survey in your email inbox,
without putting your phone number or home address on the public internet.

Stack: one `index.html` file. No build step, no dependencies, no server.
GitHub Pages hosts it free.

---

## The one thing you have to do yourself: connect the email

GitHub Pages can only serve files — it cannot send email. Formspree does that part,
and its free tier covers 50 submissions a month.

### Step 1 — Make a Formspree form

1. Go to <https://formspree.io> and sign up using **wimsattwelder@gmail.com**.
2. Click **New Form**. Name it "Welder Repair Survey."
3. Confirm the email it sends you. (Formspree will not deliver anything until you do.)
4. Formspree shows you an endpoint like:

   ```
   https://formspree.io/f/xdorwpqk
   ```

   The part after `/f/` — `xdorwpqk` in that example — is your **form ID**.

### Step 2 — Paste the ID into the site

Open `index.html`, find this line (it's around line 250, right under a comment block
that says SETUP):

```html
<form id="survey-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

Replace `YOUR_FORM_ID` with your actual ID:

```html
<form id="survey-form" action="https://formspree.io/f/xdorwpqk" method="POST">
```

Save, then commit and push:

```bash
git add index.html
git commit -m "Connect Formspree form"
git push
```

Until you do this, the form deliberately refuses to submit and shows an error
telling you the ID is still a placeholder. That's so you never think it's working
when it isn't.

### Step 3 — Turn on GitHub Pages

On the repository page on GitHub: **Settings → Pages → Source → Deploy from a branch →
`main` / `(root)` → Save.**

A minute later your site is live at:

```
https://wimsattwriter-creator.github.io/wimsatt-welder-repair/
```

### Step 4 — Test it like a customer would

Open the live site, fill the survey out yourself with fake answers, and submit.
The email should land in wimsattwelder@gmail.com within a minute or two.
**Check your spam folder the first time** — mark it "not spam" so future leads
land in your inbox where you'll see them.

---

## What's already handled

- **Your address and phone are nowhere on the site.** The survey is the gate.
  You read it, then you decide who gets your contact information.
- **Spam bots** are caught by a hidden honeypot field plus Formspree's own filtering.
- **Phones** — the layout works on a phone, which is where most of your customers
  will actually see it.
- **Rates are posted up front**: $200 for a two-hour basic on-site evaluation, plus
  48¢/mile from northern Seguin, mobile is evaluation-only, drop-off preferred, and
  repair rates get negotiated once you know what the machine needs.

## Changing the words

Everything is plain text inside `index.html`. Edit it, `git push`, and the live site
updates in about a minute. The survey questions are in the `<form>` section; the rates
are in the section that starts with `<h2>Rates`.

## If you outgrow the free tier

50 submissions a month is a lot of welder repair leads. If you ever hit it, Formspree's
paid tier is a few dollars a month — or move the form to Web3Forms, which is unlimited
and free. Either way it's a one-line change to the `action=` attribute.
