# dSIPRouter MCP Server

This repository contains the dSIPRouter MCP Server, which provides an interface to interact with dSIPRouter from conversational AI chatbots such as Claude and ChatGPT.

## Overview

The MCP (Model Context Protocol) server allows AI assistants to perform various operations on dSIPRouter, including managing endpoint groups, carrier groups, inbound mappings, and retrieving call data.

## Example Questions

Here are some example questions you can ask the AI assistant when using this MCP server:

- List the endpoint groups of dSIPRouter
- List the carrier groups of dSIPRouter
- Create a CSV file with all of the calls that happened yesterday
- List all inbound numbers

    Here's a screenshoot from Claude when asking to "list all inbound numbers"

    ![alt text](./docs/images/image.png)

## Requirements

- [dSIPRouter](https://dsiprouter.org/) 0.70 or later
- [dSIPRouter Core License](https://dopensource.com/product/dsiprouter-core-subscription-with-stirshaken/) - Contains a 7 Day Trial License

## Setup for Claude Desktop

### Using Python on Host Machine
#### Validate that the MCP Server is Working 

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   - `DSIP_BASE_URL`: The base URL of your dSIPRouter instance
   - `DSIP_TOKEN`: Your dSIPRouter API token
   - `DSIP_VERIFY_SSL`: Whether to verify SSL certificates (default: true)

3. Run the server:
   ```bash
   python main.py
   ```

   Note: You will not see any output if it's running successfully

 4. Stop the Server:

    Hit Ctrl-C twice to kill the server

 5. Configure the MCP Server for one or more conversation AI chatbots per the sections below.

 #### Configure Claude

 ##### On MacOS

1.  Open Claude Configuration File:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
 ```

2. Add the following:
```
{
  "mcpServers": {
    "dsiprouter": {
      "command": "python",
      "args": ["/full/path/to/main.py"],
      "env": {
        "DSIP_BASE_URL": "https://your-dsiprouter-server:5000",
        "DSIP_TOKEN": "your-dsiprouter-api-token",
        "DSIP_VERIFY_SSL": "true"
      }
    }
  }
}
```


3. Save the file

4. Start Claude

### Using Python using Virtual Environment (venv)
#### Validate that the MCP Server is Working 

1. Install dependencies:
   ```bash
   python -m venv .venv
   source ./.venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set environment variables:
   - `DSIP_BASE_URL`: The base URL of your dSIPRouter instance
   - `DSIP_TOKEN`: Your dSIPRouter API token
   - `DSIP_VERIFY_SSL`: Whether to verify SSL certificates (default: true)

   For example,
   ```bash
   export DSIP_BASE_URL=https://your url:5000
   export DSIP_TOKEN=your token
   export DSIP_VERIFY_SSL=true
   ```

3. Run the server:
   ```bash
   python main.py
   ```

   Note: You will not see any output if it's running successfully

 4. Stop the Server:

    Hit Ctrl-C twice to kill the server

 5. Configure the MCP Server for one or more conversation AI chatbots per the sections below.

 #### Configure Claude

 ##### On MacOS

1.  Open Claude Configuration File:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
 ```

2. Add the following:
```
{
  "mcpServers": {
    "dsiprouter": {
      "command": "<your path>/dsiprouter-mcp-server/.venv/bin/python3",
      "args": ["<your path>/code/dsiprouter-mcp-server/main.py"],
      "env": {
        "DSIP_BASE_URL": "https://your-dsiprouter-server:5000",
        "DSIP_TOKEN": "your-dsiprouter-api-token",
        "DSIP_VERIFY_SSL": "true"
      }
    }
  }
}
```


3. Save the file

4. Start Claude


## Setup for ChatGPT

### Using Python on Host Machine
#### Start the MCP Server in HTTP Mode

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   - `DSIP_BASE_URL`: The base URL of your dSIPRouter instance
   - `DSIP_TOKEN`: Your dSIPRouter API token
   - `DSIP_VERIFY_SSL`: Whether to verify SSL certificates (default: true)

3. Run the server:
   ```bash
   python main.py --http
   ```
  If you are running this on a machine with an external ip address with access to port 8000 then skipp to the next section on setting up ChatGPT

4. Expose the local server using ngrok

Open up another terminal, download ngrok, register with ngrok and start ngrok

```bash
ngrok http 8000
```

### Setting up ChatGPT to use the dSIPRouter MCP Server

1. Login to ChatGPT
2. Click Settings, then Apps
3. Enable Developer Mode
4. Click Create App
5. Enter in the basic info and for the MCP Server URL enter the ngrok external ip address and add /mcp to the end of it.  Note, select No-Authentication.  The screen should look like this

![alt text](/docs/images/chatgpt_custom_app_setup.png)

6. Click Create
7. Start a new chat and ask it a question like "list all carrier groups in dsiprouter". You will get a response like this

![alt text](/docs/images/list_of_carrier_results.png)

## Other Info

### dSIPRouter API Token

The dSIPRouter API Token is displayed after the initial install of dSIPRouter.  Their is no way to obtain your token if you didn't store it.  You can reset your dSIPRouter API Token by running this command on your dSIPRouter Server.

```bash
dsiprouter setcredentials -ac YOUR_TOKEN
```

### No valid dSIPRouter SSL Cert

If you don't have a valid SSL certificate then set DSIP_VERIFY_SSL as false