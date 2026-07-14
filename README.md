# Wimsatt Welder Repair — website

A one-page website that turns a visitor into a filled-out repair survey in your
email inbox, without putting your phone number or home address on the public
internet, and without depending on any outside company.

Live at: <https://wimsattwriter-creator.github.io/wimsatt-welder-repair/>

- **No server, no database, no third-party form service, no accounts, no monthly fee.**
- One file, `index.html`. GitHub Pages hosts it free.
- Every survey also carries a machine-readable record, so a year of jobs can
  become a spreadsheet whenever you want one.

---

## How a customer reaches you

1. They fill out the survey.
2. The page writes the email for them and hands it to their own mail program.
3. They press send. It arrives at **wimsattwelder@gmail.com**.

There is no step where a company in the middle stores your leads.

### The part people get wrong, and how this handles it

A web page **cannot tell** whether the customer's mail program actually opened.
There is no signal for it. On a phone it almost always works; on a desktop with
no mail client set up, clicking can silently do nothing.

So the page never gambles. It fires the mail program **and always shows the
finished message on screen** with a "Copy the message" button and your address.
If the mail app opened, fine — they ignore the panel. If it didn't, nothing is
lost and nothing looks broken: they copy the text and send it themselves.

A very long story won't fit in a mail link, so in that case the page sends a
short stub carrying the job number and the customer pastes the rest. Either way,
**the job number always survives.**

---

## The job number

Every survey gets one, like `WWR-2607-LKW` — year, month, and a random tag. It's
in the subject line, in the body, and in the data block.

This is the only thing tying **what came in the door** to **what the job turned
out to be worth.** Without it, your intake surveys and your finished jobs are two
unrelated piles of paper and no statistics are possible. Keep it with the job.

---

## Turning your email into statistics

At the bottom of every survey email is a block that looks like this:

```
----- WWR-DATA v1 (for record keeping - please leave this alone) -----
{"job_id":"WWR-2607-LKW","name":"Ray Tolliver","make_model":"Hobart Champion 10,000", ...}
----- END WWR-DATA -----
```

That's the same answers in a form a script can read. When you want a spreadsheet:

1. Export your welder emails out of Gmail (or just save them to a folder).
2. Run:

   ```bash
   python3 tools/intake_to_csv.py ~/Downloads/mail-export.mbox -o ~/Documents/welder-jobs.csv
   ```

It scans whatever you point it at — a folder, an `.mbox` export, loose `.eml`
files, even plain text — pulls out every data block, and writes one row per job.

### Your half of the data

The CSV ends with columns the website can't know:

| outcome | root_cause | parts_cost | hours_spent | charged | notes |
|---------|------------|------------|-------------|---------|-------|

**Fill those in yourself as jobs close.** Intake tells you what walked in; these
tell you what it was worth. Only together do they answer the questions worth
asking:

- Which machines are actually worth your time, and which ones eat a weekend?
- Do the 30-year-old Hobarts pay better than the late-model stuff?
- How often does "somebody already worked on it" predict a job going sideways?
- Is a jump-started machine a reliable tell for a blown rectifier?
- Which towns are worth the drive at 48¢ a mile, and which never are?

**Re-running the script will not erase what you typed.** It merges on the job
number and leaves your columns alone.

### Where the spreadsheet lives

**Outside this repository.** It has customer names, emails, and phone numbers in
it. That is business records, not website content, and it must never be pushed to
a public repo — same rule as the W9.

---

## Changing the words

Everything is plain text in `index.html`. Edit it, then:

```bash
git add -A && git commit -m "what changed" && git push
```

The live site updates in about a minute. The survey questions are inside the
`<form>`; the rates are in the section starting `<h2>Rates`.

If you add a new survey question, add its field name to `INTAKE_FIELDS` in
`tools/intake_to_csv.py` so it becomes a spreadsheet column too.

---

## What's posted on the site

Drop-off strongly preferred (northern Seguin). Mobile is **evaluation only** —
$200 for two hours plus 48¢/mile, and the customer has to be close. Repair rates
get worked out between you and them once the machine's problem is known.
