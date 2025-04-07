# App Agent & Assistant Template (Bolt for Python)

This Bolt for Python template demonstrates how to build [Agents & Assistants](https://api.slack.com/docs/apps/ai) in Slack.

## Setup

Before getting started, make sure you have a development workspace where you have permissions to install apps. If you don't have one setup, go ahead and [create one](https://slack.com/create).

### Developer Program

Join the [Slack Developer Program](https://api.slack.com/developer-program) for exclusive access to sandbox environments for building and testing your apps, tooling, and resources created to help you build and grow.

## Installation

#### Create a Slack App

1. Open [https://api.slack.com/apps/new](https://api.slack.com/apps/new) and choose "From an app manifest"
2. Choose the workspace you want to install the application to
3. Copy the contents of [manifest.json](./manifest.json) into the text box that says `*Paste your manifest code here*` (within the JSON tab) and click *Next*
4. Review the configuration and click *Create*
5. Click *Install to Workspace* and *Allow* on the screen that follows. You'll then be redirected to the App Configuration dashboard.

#### Environment Variables

Before you can run the app, you'll need to store some environment variables.

1. Open your app configuration page from this list, click **OAuth & Permissions** in the left hand menu, then copy the Bot User OAuth Token. You will store this in your environment as `SLACK_BOT_TOKEN`.
2. Click **Basic Information** from the left hand menu and follow the steps in the App-Level Tokens section to create an app-level token with the `connections:write` scope. Copy this token. You will store this in your environment as `SLACK_APP_TOKEN`.

```zsh
# Replace with your app token and bot token
# For Windows OS, env:SLACK_BOT_TOKEN = <your-bot-token> works
export SLACK_BOT_TOKEN=<your-bot-token>
export SLACK_APP_TOKEN=<your-app-token>
# This sample uses OpenAI's API by default, but you can switch to any other solution!
export OPENAI_API_KEY=<your-openai-api-key>
```

### Setup Your Local Project

```zsh
# Clone this project onto your machine
git clone https://github.com/slack-samples/bolt-python-assistant-template.git

# Change into this project directory
cd bolt-python-assistant-template

# Setup your python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # for Windows OS, .\.venv\Scripts\Activate instead should work

# Install the dependencies
pip install -r requirements.txt

# Start your local server
python3 app.py
```

#### Linting

```zsh
# Run flake8 from root directory for linting
flake8 *.py && flake8 listeners/

# Run black from root directory for code formatting
black .
```

## Project Structure

### `manifest.json`

`manifest.json` is a configuration for Slack apps. With a manifest, you can create an app with a pre-defined configuration, or adjust the configuration of an existing app.

### `app.py`

`app.py` is the entry point for the application and is the file you'll run to start the server. This project aims to keep this file as thin as possible, primarily using it as a way to route inbound requests.

### `/listeners`

Every incoming request is routed to a "listener". Inside this directory, we group each listener based on the Slack Platform feature used, so `/listeners/events` handles incoming events, `/listeners/shortcuts` would handle incoming [Shortcuts](https://api.slack.com/interactivity/shortcuts) requests, and so on.

## App Distribution / OAuth

Only implement OAuth if you plan to distribute your application across multiple workspaces. A separate `app_oauth.py` file can be found with relevant OAuth settings.

When using OAuth, Slack requires a public URL where it can send requests. In this template app, we've used [`ngrok`](https://ngrok.com/download). Checkout [this guide](https://ngrok.com/docs#getting-started-expose) for setting it up.

Start `ngrok` to access the app on an external network and create a redirect URL for OAuth.

```
ngrok http 3000
```

This output should include a forwarding address for `http` and `https` (we'll use `https`). It should look something like the following:

```
Forwarding   https://3cb89939.ngrok.io -> http://localhost:3000
```

Navigate to **OAuth & Permissions** in your app configuration and click **Add a Redirect URL**. The redirect URL should be set to your `ngrok` forwarding address with the `slack/oauth_redirect` path appended. For example:

```
https://3cb89939.ngrok.io/slack/oauth_redirect
```

Run Deployment on AWS Lambda:

```
<!-- lambda deploy \
  --config-file lazy_aws_lambda_config.yaml \
  --requirements requirements.txt -->

sam build && sam deploy --no-resolve-s3
```

# Slack App with AWS SAM

This is a Slack application that uses AWS SAM for serverless deployment and integrates with OpenAI for intelligent responses.

## Project Structure

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

## Prerequisites

- Python 3.11+
- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- Slack App with Socket Mode enabled
- OpenAI API key

## Local Development

1. Install AWS SAM CLI:

   ```bash
   pip install aws-sam-cli
   ```

2. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your credentials:

   ```bash
   cp .env.example .env
   ```

4. Run locally:

   ```bash
   sam local start-api
   ```

## AWS SAM Deployment

### Setup

1. Configure AWS CLI:

   ```bash
   aws configure
   ```

2. Create an S3 bucket for deployment (if needed):

   ```bash
   aws s3 mb s3://slack-app-deployment
   ```

3. Update `samconfig.toml` with your credentials:

   ```bash
   # Edit samconfig.toml and update the parameter_overrides with your actual tokens
   ```

4. Build and Deploy using SAM:

   ```bash
   # Build the application
   sam build
   
   # Deploy the application
   sam deploy --guided
   ```

### Standard Deployment Process

With the new project structure, you can follow the standard SAM workflow:

```bash
# Build the application
sam build

# Deploy to AWS
sam deploy --guided

# Or if you've already run guided deployment
sam deploy
```

SAM will:

1. Package your source code
2. Create the necessary AWS resources
3. Deploy the Lambda function
4. Set up the API Gateway
5. Configure environment variables

### Environment Variables

- `SLACK_APP_TOKEN`: Your Slack App-level token (starts with xapp-)
- `SLACK_BOT_TOKEN`: Your Slack Bot User OAuth Token (starts with xoxb-)
- `OPENAI_API_KEY`: Your OpenAI API key
- `SLACK_SIGNING_SECRET`: Your Slack App's signing secret

## Setting up Slack App

1. Create a new Slack App at <https://api.slack.com/apps>
2. Enable Socket Mode
3. Add the following Event Subscriptions:
   - `message.channels`
   - `app_mention`
4. Add a slash command `/ask`
5. Install the app to your workspace
6. Copy the tokens to your samconfig.toml file
7. Update the Event Subscription URL with your API Gateway URL after deployment

## Architecture

The application uses:

- AWS Lambda for serverless deployment
- AWS SAM for infrastructure as code
- API Gateway for HTTP endpoints
- Slack Bolt framework for Slack integration
- OpenAI for generating responses

## Monitoring

Monitor your application using:

- AWS CloudWatch Logs
- AWS CloudWatch Metrics
- Slack Event logs

## Troubleshooting

1. Check CloudWatch Logs:

   ```bash
   sam logs -n SlackAppFunction --stack-name slack-app
   ```

2. Verify Lambda function:

   ```bash
   aws lambda invoke --function-name slack-app-SlackAppFunction-XXXX response.json
   ```

3. Check Slack App settings:
   - Verify Event Subscriptions URL
   - Check token permissions
   - Monitor WebSocket connections

## Security Considerations

- All sensitive tokens are stored as SAM parameters
- HTTPS is enforced through API Gateway
- Minimal required permissions are used
- Regular security updates are applied

## Cost Optimization

- Use Lambda provisioned concurrency for consistent performance
- Monitor and adjust memory allocation
- Use CloudWatch alarms for cost monitoring
- Implement proper error handling to avoid unnecessary executions

## Cleanup

To delete the deployed application:

```bash
sam delete
```
