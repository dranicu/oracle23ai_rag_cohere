# oracle23ai_rag_cohere

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Dependencies](#dependencies)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Overview

This repository demonstrates how to build a Retrieval-Augmented Generation (RAG) system using Cohere's API to enhance conversational AI. The system integrates external knowledge sources to provide relevant responses to user queries.

## Prerequsites

OCI Vault(OCID of this resource) created with the admin password for the ADB in a secret. Proper IAM permission set to access the Vault.(Password must start with a letter, be 12 characters long, conatin at least one upper case letter and two digits and no special characters)

## Installation

Deploy the infrastructure necessary to run this example in OCI by using the following git repo: https://github.com/dranicu/terraform-oke-ora23ai.git.

## Usage

1. Use the link output provided by the stack in the instalation step to access the JupyterHUB.
2. Go to "examples" folder
3. In the ora23ai_connection.py file use the ocids of the vault secret where you stored the ADMIN password for ADB and the ocid of the ADB(MARKED WITH <PLACEHOLDER>)
4. Run the cohere-rag-ora23ai-chatbot.ipynb. Shift+Enter on each section to avoid any errors.
5. Once the Gradio interface is up and running, paste your cohere api key in the llm and embedding sections
6. Upload a file and create a vector store.
7. Load the cohere LLM model and ask any question from the files you uploaded.

## File Descriptions

- `cohere-rag-ora23ai-chatbot.ipynb`: Contains the chatbot implementation.
- `ora23ai_connection.py`: Manages the connection to Oracle 23 AI services.
- `ora23ai_gradio_chatbot.py`: Gradio interface for user interaction.
- `ora23ai_model_index.py`: Handles model indexing.
- `ora23ai_model_utils.py`: Utility functions for model management.

## Dependencies

The project relies on the following dependencies listed in `requirements.txt`:
- cohere
- gradio
- python-dotenv
- other necessary libraries.

Install them using:
```
pip install -r requirements.txt
```


## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Feel free to open a pull request or issue for bug fixes, features, or improvements.

## Acknowledgements

Special thanks to:
- [Cohere](https://cohere.ai/) for their NLP models.
- [Gradio](https://gradio.app/) for simplifying web-based interfaces.