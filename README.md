# Gitogether 🤝

A platform where developers find each other. Post a project, discover collaborators, and build something together.

---

## What is this?

Finding the right person to build with is hard. Gitogether makes it simple — create a profile, post your project, and connect with developers whose skills match what you need. No endless scrolling through job boards, no cold emails. Just developers looking for the same thing you are.

---

## Features

- **Developer Profiles** — showcase your skills, experience, and how to reach you
- **Post Projects** — describe what you're building and what kind of collaborator you need
- **Browse & Filter** — find projects or developers by skill, sorted by reputation
- **Request to Join** — send a join request, owner reviews and accepts or rejects
- **Collaboration Tracking** — active and completed projects all in one place
- **Ratings** — rate your collaborators after a project wraps up, build your reputation over time

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | PostgreSQL (hosted on Supabase) |
| DB Driver | psycopg2 |

---

## Project Structure

```
gitogether/
├── app.py                  # Entry point
├── config.py               # Environment config
├── .env                    # Credentials (not committed)
├── requirements.txt
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── dashboard/
│   ├── projects/
│   ├── developers/
│   ├── matches/
│   └── admin/
├── models/
│   ├── db.py
│   ├── user.py
│   ├── project.py
│   ├── skill.py
│   ├── request.py
│   ├── match.py
│   └── rating.py
├── controllers/
│   ├── auth.py
│   ├── dashboard.py
│   ├── projects.py
│   ├── developers.py
│   ├── requests.py
│   ├── matches.py
│   ├── ratings.py
│   └── admin.py
└── sql/
    ├── schema.sql
    ├── views.sql
    └── seed.sql
```

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/your-username/gitogether.git
cd gitogether
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your `.env` file**
```
DATABASE_URL=postgresql://postgres:[password]@[host].supabase.co:5432/postgres
SECRET_KEY=your_secret_key_here
DEBUG=True
```

**5. Run the schema on Supabase**

Go to your Supabase project → SQL Editor → paste the contents of `sql/schema.sql` → Run.

**6. Start the app**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## Contributors

| Name | GitHub |
|------|--------|
| AnasKhan | [@AnasKhan](https://github.com/AnasKhan-1) |
| AreebSaeed | [@AreebSaeed](https://github.com/AreebSaeed) |

---
