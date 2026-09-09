# Email assets

Images for the EmailOctopus campaigns and automations, hosted here so the
newsletter loads its pictures from the same domain it is sent from, and so the
URLs never change out from under a campaign that has already gone out.

Paste these URLs straight into the EmailOctopus editor:

| File | URL | Insert at |
|---|---|---|
| `logo.png` | `https://beyondtheleashwithsandra.com/email/logo.png` | 160 px wide |
| `icon-linkedin.png` | `https://beyondtheleashwithsandra.com/email/icon-linkedin.png` | 32 px wide |
| `icon-website.png` | `https://beyondtheleashwithsandra.com/email/icon-website.png` | 32 px wide |

Every file is drawn at 2x-3x its display size so it stays sharp on retina
screens, and is flattened onto white rather than left transparent — a fair
number of mail clients drop the alpha channel and would otherwise render the
logo on black.

`logo.png` is generated from `../images/logo.png`. The two icons are drawn by
`make-icons.py` in this folder; rerun it if the brand navy ever changes.
