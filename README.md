# Unparsed 2024 Talk

Welcome to the repository for the "Unparsed 2024 Talk" by Roger Kibbe. This repository contains all the materials and resources for the presentation delivered at the Unparsed 2024 conference.

## Table of Contents

- [Introduction](#introduction)
- [Presentation Slides](#presentation-slides)
- [Code Examples](#code-examples)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

This repository hosts the content for Roger Kibbe's talk at Unparsed 2024. The presentation explores the differences between prompt engineering, RAG and fine-tuning and explores the when, what and how of fine-tuning LLM

## Presentation Slides

The presentation slides can be found in the `presentation` directory.
- [Presentation](/presentation/Unparsed%2024%20Presentation%20-%20Fine%20Tuning.pdf)


## Code Examples

[Mistral 7B Fine Tune Juypter Notebook](mistral_finetune.ipynb)

[Fine-Tuning Data](bofh_training_data_mistral.jsonl)

[Simple Mistral CLI chatbot](cli_compare.py)

[Simple Mistral GUI Chatbot](gui_client.py)

## Installation

To run the code examples locally, you will need to have Python installed. Follow the instructions below to set up your environment:

1. Clone the repository:
    ```bash
    git clone https://github.com/rogerkibbe/unparsed-2024-talk.git
    cd unparsed-2024-talk
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
4. Get a [Mistral API key](https://console.mistral.ai/api-keys/#) and create a .env file with the key:
```
MISTRAL_API_KEY=[Mistral API Key]
```
## Usage

The fine-tuning code is located in the [mistral_finetune.ipynb](mistral_finetune.ipynb) Juypter notebook. Open it to run the fine-tune.

The fine-tuning data is IT support Q&A for a [Bastard Operator from Hell](https://en.wikipedia.org/wiki/Bastard_Operator_From_Hell) type chatbot. The data was created by Anthropic's Claude and hand edited.

Both [cli_compare.py](cli_compare.py) and [gui_client.py](gui_client.py) are python panel apps. To run them:
```
panel serve [file name]
```
