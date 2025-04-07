# Project Structure

```
slack-app/
│
├── src/                        # Source code
│   ├── app.py                  # Lambda handler function
│   ├── listeners/              # Slack event listeners
│   │   ├── __init__.py
│   │   ├── agent.py            # Agent definitions
│   │   ├── events.py           # Event handlers
│   │   ├── commands.py         # Command handlers
│   │   └── llm_caller.py       # LLM integration
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── helpers.py
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   └── test_app.py
│
├── template.yaml               # SAM template
├── samconfig.toml              # SAM configuration
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
└── README.md                   # Project documentation
```
