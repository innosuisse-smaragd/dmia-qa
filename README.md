# DMIA-Q&A

DMIA-QA is an application that maps user questions to a predefined collection of question-answer pairs based on similarity of sentence embeddings.

The application is based on the sentence-transformers library. It creates embeddings for all predefined questions. It then calculates the cosine distance between the embedded user question and all predefined questions.

A highest-vote approach is followed, enabling the specification of multiple models to be used. The system is designed that each model might output a different variation of a question, however referring to the same answer.

Currently, an answer is provided only if the distance is smaller than 0.7 and the user input is at least four words long.

## Installation

Build and run a docker image from the root directory:

```bash
docker build -t dmia-qa .
docker run -dp <HOST-PORT>:5000 dmia-qa
```

## Usage

Make a HTTP POST request to /answer containing the user question to be mapped as raw json body:

```json
{
  "text": "Tut eine Mammographie weh?"
}
```

The application returns the answer to the most similar predefined question (HTTP 200 OK).

#### Error responses

- 400 BAD REQUEST: The input is too short (minimum of four words).
- 501 NOT IMPLEMENTED: There was no question found which was similar enough to the user input
