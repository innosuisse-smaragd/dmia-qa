# DMIA-Q&A

DMIA-QA is an application that maps user questions to a predefined collection of question-answer pairs based on similarity of sentence embeddings.

The application is based on the sentence-transformers library. It creates embeddings for all predefined questions. It then calculates the cosine distance between the embedded user question and all predefined questions.

Among the top 5 similar questions variations, either the most common answer or a unique answer to the most similar question is looked up and returned.

Currently, an answer is provided only if the distance (cosine similarity) is smaller than 0.7 and the user input is at least four words long.

## Installation

Build and run a docker image from the root directory:

```bash
docker build -t dmia-qa .
docker run -dp <HOST-PORT>:5000 dmia-qa
```

## Usage

### GET answer

Make a HTTP GET request to /answer containing the user question to be mapped as raw json body. Choose application/json as Content-Type header.

```json
{
  "text": "Tut eine Mammographie weh?"
}
```

The application returns the answer to the most similar predefined question (HTTP 200 OK).

#### Error responses

- 400 BAD REQUEST: The input is too short (minimum of four words).
- 501 NOT IMPLEMENTED: There was no question found which was similar enough to the user input

### POST wrong answer to question

Make a HTTP POST request to /improve containing the user question and the wrong answer as a raw json body. Choose application/json as Content-Type header.

```json
{
  "question": "Tut eine Mammografie weh?",
  "wrongAnswer": "Eine Mammografie ist nicht kostenlos"
}
```

The application returns HTTP 200 OK.

#### Error responses

Not applicable

## Open issues

- [ ] Initially, a multi-model voting system was implemented. However, it was changed to using only the output of the first model.
- [ ] Improve method of determining if found questions are similar enough- right now, the first (== best) result of the collection.query method just needs to be below a cosing distance of 0.7.
- [ ] When aggregating the most common answer within the results, an exact string match is carried out. This might lead to errors when answers are not completetly identical.
