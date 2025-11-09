# Quick Start Guide

Get started with the Educational Assistant in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up OpenAI API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

## Step 3: Run the Demo

```bash
# See the system capabilities without API calls
python demo.py
```

## Step 4: Run Tests

```bash
# Verify everything works
python tests/test_basic.py
```

## Step 5: Try It Out!

### Option A: Interactive Mode (Recommended)
```bash
python main.py interactive --path examples/lecture_materials
```

Then ask questions like:
- "What is machine learning?"
- "Explain supervised learning"
- "What are neural networks?"

Type `feedback` to provide feedback on responses.
Type `quit` to exit.

### Option B: Single Question
```bash
python main.py ask \
  --path examples/lecture_materials \
  --question "What is machine learning?"
```

### Option C: Python API
```python
from src.educational_assistant import EducationalAssistant

# Initialize
assistant = EducationalAssistant()

# Load documents
assistant.ingest_documents("examples/lecture_materials")

# Ask a question
result = assistant.ask("What is machine learning?")
print(result['answer'])
```

## Add Your Own Documents

1. Add PDF, DOCX, PPTX, or TXT files to `examples/lecture_materials/`
2. Run the ingest command:
   ```bash
   python main.py ingest --path examples/lecture_materials --save vector_store
   ```
3. Use the saved vector store:
   ```bash
   python main.py ask --load vector_store --question "Your question here"
   ```

## Troubleshooting

### "No module named 'src'"
Make sure you're in the project root directory when running commands.

### "OPENAI_API_KEY not found"
Make sure you've created a `.env` file with your API key.

### Dependencies not installing
Try: `pip install --upgrade pip` then retry `pip install -r requirements.txt`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [examples/example_usage.py](examples/example_usage.py) for more examples
- Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details

## Need Help?

Open an issue on GitHub with:
- What you're trying to do
- The error message (if any)
- Your Python version (`python --version`)
