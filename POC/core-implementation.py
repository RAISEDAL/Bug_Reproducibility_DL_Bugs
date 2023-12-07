import streamlit as st
import requests
import json
from sentence_transformers import SentenceTransformer, util
import pandas as pd
st.set_page_config(layout="wide")

def main():
    st.title("DLRepro: Improving the Reproducibility of Deep Learning Bugs")
    page = st.radio(
        "Select a page",
        [
            "Edit Actions Recommender",
            "Our findings on Deep Learning Bug Reproducibility",
        ],
    )

    if page == "Our findings on Deep Learning Bug Reproducibility":
        home_page()
    elif page == "Edit Actions Recommender":
        recommendation_page()

def home_page():
    st.header(
        "Relationship between Critical Information and Type of Bug"
    )
    st.markdown(
        "This table illustrates the critical information needed to reproduce specific types of deep learning bugs."
    )
    critical_information_table_data = {
        "Model": ["Logs", "Neural Network", "Code Snippet"],
        "Tensor": ["Data", "Logs", "Code Snippet"],
        "Training": ["Code Snippet", "Logs", "Data"],
        "API": ["Logs", "Code Snippet", "Model"],
    }
    critical_information_df = pd.DataFrame(critical_information_table_data)
    st.dataframe(critical_information_df, hide_index=True)
    st.caption("Table 1: Relationship between Critical Information and Types of Deep Learning Bugs")

    st.header("Relationship between Edit Actions and Type of Bug")
    st.markdown(
        "This table demonstrates the different of edit actions that can be used to reproduce specifc types of deep learning bugs."
    )
    edit_actions_table_data = {
        "Model": [
            "Neural Network Definition",
            "Import Addition",
            "Hyperparameter Initialization",
            "Logging",
            "Dataset Procurement",
        ],
        "Tensor": [
            "Import Addition",
            "Input Data Generation",
            "Hyperparameter Initialization",
            "Dataset Procurement",
            "Logging",
        ],
        "Training": [
            "Input Data Generation",
            "Import Addition",
            "Version Migration",
            "Hyperparameter Initialization",
            "Compiler Error Resolution",
        ],
        "API": [
            "Input Data Generation",
            "Hyperparameter Initialization",
            "Import Addition",
            "Logging",
            "Obsolete Parameter Removal",
        ],
    }
    edit_actions_df = pd.DataFrame(edit_actions_table_data)
    st.dataframe(edit_actions_df, hide_index=True)
    st.caption("Table 2: Relationship between Edit Actions and Type of Deep Learning Bug")

def recommendation_page():

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load data
    with open("./tags.json") as f:
        tags = json.load(f)

    with open("./critical_information.json") as f:
        critical_information = json.load(f)

    with open("./edit_actions.json") as f:
        edit_actions = json.load(f)

    # Get question ID from user input
    id = st.text_input("Enter the Stack Overflow question ID: (e.g., 50920908)")

    # Process the question
    if st.button("Recommend Edit Actions and Critical Information"):
        classify_bug(id, tags, model, critical_information, edit_actions)


def classify_bug(id, tags, model, critical_information, edit_actions):
    with st.spinner("Retrieving the Stack Overflow Data"):
        url = f"https://api.stackexchange.com/2.3/questions/{id}?order=desc&sort=activity&site=stackoverflow&key=vc5m5jBpRA2Rw0HanS2XsA(("

        response = requests.get(url.format(id=id))
        response_object = response.json()
        question_tags = response_object["items"][0]["tags"]

        type_of_bug = "-"
        tag_to_bug_type = {
            "model": "model",
            "training": "training",
            "api": "api",
            "tensor": "tensor"
        }
        exact_match_found = True
        with st.spinner("Determining the Type of Bug"):
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
                }
                scores = {
                    tag: util.pytorch_cos_sim(model.encode(question_tags), embedding)
                    for tag, embedding in tag_embeddings.items()
                }
                type_of_bug = max(scores, key=lambda x: scores[x].max())
        type_of_bug = type_of_bug.capitalize() if type_of_bug != 'api' else 'API'
        with st.spinner("Preparing the Recommendations"):
            result_text = ""
            if exact_match_found:
                result_text += f"The type of bug is: **{type_of_bug}**"
            else:
                result_text += f"The type of bug might be: **{type_of_bug}**"
            st.markdown(result_text)

            # Instead of appending it as a text, I want it to be st.expander()
            result_text = "\n\nTo reproduce the bug, the most critical information needed is:"
            st.markdown(result_text)
            for info in critical_information[type_of_bug]:
                expander = st.expander("**{}**".format(info.split(":")[0]))
                expander.write("{}".format(info.split(":")[1]))

            result_text = "\n\nTo reproduce the bug, we can use the following edit actions:"
            st.markdown(result_text)
            for action in edit_actions[type_of_bug]:
                expander = st.expander("**{}**".format(action.split(":")[0]))
                expander.write("{}".format(action.split(":")[1]))
                edit_action = action.split(":")[0]
                if edit_action in ["Hyperparameter Initialization", "Input Data Generation", "Logging", "Neural Network Definition", "Version Migration"]:
                    file = open("./code-snippets/{}.py".format(edit_action), "r")
                    code = file.read()
                    expander.code(code, language="python")

if __name__ == "__main__":
    main()
