from sentence_transformers import SentenceTransformer
import chromadb
import Question
import load_data
from collections import Counter


class Model:
    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.questions = Question.read_csv("./raw/questions.csv")
        self.model_names = load_data.load_text(file_path="./raw/models.txt")
        self.models = []
        self.collections = []
        self.initialize_models()
        for model_name, model in self.models:
            collection = self.__compute_store_embeddings(model_name, model)
            self.collections.append(collection)
        print("Model initialized - ready for prediction.")

    def predict(self, text):
        input_lenth = len(text.split())
        if input_lenth < 4:
            raise ValueError()
        raw_result = self.__compute_similarities(text)
        print(raw_result)
        # only takes first model result from here
        if not self.__results_have_enough_similarity(raw_result[0]):
            self.__save_unanswerable_question(text)
            raise NotImplementedError()
        result = self.__answer_max_vote(raw_result[0])
        return result

    def save_wrong_prediction(self, text):
        with open("./raw/wrongClassifications.csv", "a") as file:
            string = text["question"] + ", " + text["wrongAnswer"] + "\n"
            file.write(string)
        return

    @staticmethod
    def __save_unanswerable_question(question):
        print("qeuestion", question)
        with open("./raw/missingAnswers.txt", "a") as file:
            string = question + "\n"
            file.write(string)
        return

    def initialize_models(self):
        for model_name in self.model_names:
            model = SentenceTransformer(model_name)
            tuple = (model_name, model)
            self.models.append(tuple)

    def __compute_store_embeddings(self, full_model_name, model, distance="cosine"):
        # Encode all sentences
        splitted_model_name = full_model_name.split("/")
        model_name = splitted_model_name[-1]
        collection_name = "collection_" + model_name
        collection = self.chroma_client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": distance}
        )  # l2, ip
        texts = [getattr(question, "text") for question in self.questions]
        ids = [getattr(question, "id") for question in self.questions]
        embeddings = model.encode(texts)
        list_of_embeddings = [tensor.tolist() for tensor in embeddings]

        collection.upsert(embeddings=list_of_embeddings, documents=texts, ids=ids)
        return collection

    @staticmethod
    def __embed_user_question(model, user_question):
        user_question_emb = model.encode(user_question)
        return user_question_emb

    @staticmethod
    def __get_nearest_neighbour(collection, user_question_emb, n_results=5):
        result = collection.query(
            query_embeddings=user_question_emb.tolist(), n_results=n_results
        )
        return result

    def __compute_similarities(self, user_question):
        results = []
        for index, (name, model) in enumerate(self.models):
            user_question_emb = self.__embed_user_question(model, user_question)
            query_result = self.__get_nearest_neighbour(
                self.collections[index], user_question_emb
            )

            results.append(query_result)

        return results

    @staticmethod
    def __restructure_dict(dict_to_structure):
        restructured_dict = {}

        # Iterate over the list of dictionaries
        for item in dict_to_structure:
            # Iterate over the keys in each dictionary
            for key, value in item.items():
                # Check if the value is None
                if value is not None:
                    # Check if the value is subscriptable
                    if len(value) > 0 and len(value[0]) > 0:
                        # Check if the key already exists in the restructured dictionary
                        if key in restructured_dict:
                            restructured_dict[key].append(value[0][0])
                        else:
                            restructured_dict[key] = [value[0][0]]
        return restructured_dict

    def __answer_max_vote(self, result):
        filtered_questions = []
        for id in result["ids"][0]:
            for question in self.questions:
                if question.id == id:
                    filtered_questions.append(question)
        return self.__get_most_common_attribute(filtered_questions, "answer")

    @staticmethod
    def __get_most_common_attribute(questions, attribute):
        attribute_values = [getattr(obj, attribute) for obj in questions]
        attribute_counts = Counter(attribute_values)
        most_common_attribute = attribute_counts.most_common(1)[0][0]
        return most_common_attribute

    @staticmethod
    def __results_have_enough_similarity(raw_result):
        has_enough_similarity = True
        distances = raw_result["distances"][0]
        if min(distances) > 0.7:
            has_enough_similarity = False
        return has_enough_similarity
