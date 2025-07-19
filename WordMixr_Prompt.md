# WordMixr – Full-Stack Web App Prompt

Create a full-stack web application called **WordMixr**, designed to help users solve word puzzles by rearranging scrambled letters. It should support solving anagrams and subword puzzles using a dictionary of English words. The app should be fully containerized using Docker.

## 📁 Project Structure
Use the following directory layout:

```
wordmixr/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── solver.py
│   │   └── utils.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── components/
│   │       └── WordSolver.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── docker-compose.yml
├── README.md
└── screenshots/
    └── ui_mockup.png
```

## 🔙 Backend (Python + FastAPI)
- Use **FastAPI** with Python 3.11.
- Create an endpoint: `GET /solve?letters=abcde`
  - Accepts a string of letters.
  - Returns all valid English words that can be formed using those letters.
  - Ignore permutations with repeating letters not present in the input.
- Use a fast anagram solving algorithm based on `collections.Counter` and `set` membership for word dictionary lookups.

### Dependencies (`requirements.txt`)

```
fastapi
uvicorn[standard]
python-multipart
```

### Example Word Solver Logic (backend/app/solver.py)
```python
from collections import Counter

def load_dictionary(filepath="words_alpha.txt"):
    with open(filepath, "r") as f:
        return set(word.strip().lower() for word in f)

def find_valid_words(letters, dictionary):
    letter_count = Counter(letters.lower())
    valid_words = set()
    for word in dictionary:
        word_count = Counter(word)
        if all(word_count[char] <= letter_count[char] for char in word_count):
            valid_words.add(word)
    return sorted(valid_words)
```

## 🖥️ Frontend (React + TypeScript)
- Use **Vite** or **Create React App** with TypeScript.
- Create a component `<WordSolver />`:
  - Input field to type scrambled letters.
  - “Solve” button to query the backend.
  - Result list of valid words.
- Use `axios` or `fetch()` to connect to the backend.

### Suggested Component Layout
```tsx
function WordSolver() {
  const [letters, setLetters] = useState("");
  const [words, setWords] = useState([]);

  const solve = async () => {
    const res = await fetch(`/solve?letters=${letters}`);
    const data = await res.json();
    setWords(data.words);
  };

  return (
    <div>
      <h1>WordMixr</h1>
      <input value={letters} onChange={e => setLetters(e.target.value)} />
      <button onClick={solve}>Solve</button>
      <ul>{words.map(w => <li key={w}>{w}</li>)}</ul>
    </div>
  );
}
```

## 🐳 Docker Setup
### Backend Dockerfile (`backend/Dockerfile`)
```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile (`frontend/Dockerfile`)
```Dockerfile
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
RUN npm install -g serve
CMD ["serve", "-s", "dist"]
```

### Docker Compose (`docker-compose.yml`)
```yaml
version: "3.9"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - CHOKIDAR_USEPOLLING=true
```

## 📂 Word List
Use a dictionary like `words_alpha.txt` from:
https://github.com/dwyl/english-words

Place it in the `backend/app/` directory and load it at startup.

## 🧪 Testing
- Visit `http://localhost:3000`
- Enter a scrambled letter set (e.g., `scramble`) and click “Solve”
- Words are fetched from the FastAPI backend and listed in the UI
