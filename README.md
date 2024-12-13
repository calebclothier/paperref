# PaperRef

## Getting Started

### Installing uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Getting untracked environment files

Contact [Caleb](https://github.com/calebclothier) to obtain the following untracked environment files:

1. `backend/app/.env`
2. `frontend/src/.streamlit/secrets.toml`

### Starting the backend server

   ```bash
   cd backend
   uv run fastapi dev
   ```

### Starting the frontend web app

   ```bash
   cd frontend/src
   uv run streamlit run Home.py
   ```
