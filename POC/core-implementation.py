import streamlit as st
import requests
import json
from sentence_transformers import SentenceTransformer, util

import streamlit as st
import requests
import json
from sentence_transformers import SentenceTransformer, util


def main():
    st.title("DLRepro: Improving the Reproducibility of Deep Learning Bugs")

    # Add navigation to the sidebar
    page = st.sidebar.selectbox(
        "Select a page",
        [
            "Our findings on Deep Learning Bug Reproducibility",
            "Edit Actions Recommender",
        ],
    )

    if page == "Our findings on Deep Learning Bug Reproducibility":
        home_page()
    elif page == "Edit Actions Recommender":
        recommendation_page()


def home_page():
    st.write("Our findings on Deep Learning Bug Reproducibility")

    st.header(
        "Relationship between Critical Information and Types of Deep Learning Bugs"
    )
    critical_information_table_data = {
        "Model": ["Logs", "Neural Network", "Code Snippet"],
        "Tensor": ["Data", "Logs", "Code Snippet"],
        "Training": ["Code Snippet", "Logs", "Data"],
        "API": ["Logs", "Code Snippet", "Model"],
    }
    st.table(critical_information_table_data)

    st.header("Relationship between Edit Actions and Type of Bug")
    edit_actions_table_data = {
        "model": [
            "Neural Network Definition",
            "Import Addition",
            "Hyperparameter Initialization",
            "Logging",
            "Dataset Procurement",
        ],
        "tensor": [
            "Import Addition",
            "Input Data Generation",
            "Hyperparameter Initialization",
            "Dataset Procurement",
            "Logging",
        ],
        "training": [
            "Input Data Generation",
            "Import Addition",
            "Version Migration",
            "Hyperparameter Initialization",
            "Compiler Error Resolution",
        ],
        "api": [
            "Input Data Generation",
            "Hyperparameter Initialization",
            "Import Addition",
            "Logging",
            "Obsolete Parameter Removal",
        ],
    }
    st.table(edit_actions_table_data)


def recommendation_page():
    st.write("Edit Actions Recommender")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load data
    with open("tags.json") as f:
        tags = json.load(f)

    with open("critical_information.json") as f:
        critical_information = json.load(f)

    with open("edit_actions.json") as f:
        edit_actions = json.load(f)

    # Get question ID from user input
    id = st.text_input("Enter the question ID:")

    # Process the question
    if st.button("Recommend Edit Actions and Critical Information"):
        classify_bug(id, tags, model, critical_information, edit_actions)


def classify_bug(id, tags, model, critical_information, edit_actions):
    url = f"https://api.stackexchange.com/2.3/questions/{id}?order=desc&sort=activity&site=stackoverflow&key=vc5m5jBpRA2Rw0HanS2XsA(("

    response = requests.get(url.format(id=id))

    response_object = response.json()
    question_tags = response_object["items"][0]["tags"]

    type_of_bug = "-"
    tag_to_bug_type = {
        "model": "model",
        "training": "training",
        "api": "data",
        "tensor": "tensor",
        "gpu": "gpu",
    }
    exact_match_found = True

    for tag in question_tags:
        for bug_type, bug_tags in tags.items():
            if tag in bug_tags:
                type_of_bug = tag_to_bug_type[bug_type]
                break

    if type_of_bug == "-":
        exact_match_found = False
        tag_embeddings = {
            "model": model.encode(tags["model"]),
            "training": model.encode(tags["training"]),
            "api": model.encode(tags["api"]),
            "tensor": model.encode(tags["tensor"]),
            "gpu": model.encode(tags["gpu"]),
        }
        scores = {
            tag: util.pytorch_cos_sim(model.encode(question_tags), embedding)
            for tag, embedding in tag_embeddings.items()
        }
        type_of_bug = max(scores, key=lambda x: scores[x].max())

    result_text = ""
    if exact_match_found:
        result_text += f"The type of bug is: {type_of_bug.capitalize()}"
    else:
        result_text += f"The type of bug might be: {type_of_bug.capitalize()}"

    result_text += "\n\nTo reproduce the bug, the most critical information needed is:"
    for info in critical_information[type_of_bug]:
        result_text += f"\n- {info}"

    result_text += "\n\nTo reproduce the bug, we can use the following edit actions:"
    for action in edit_actions[type_of_bug]:
        result_text += f"\n- {action}"

    st.text(result_text)


if __name__ == "__main__":
    main()
