## Bug Reproducibility for Deep Learning Systems

This repository is the replication package for the project "Enhancing the Reproducibility of Deep Learning Bugs: An Empirical Study". This study is conducted under the supervision and guidance of Dr. Masud Rahman and Dr. Foutse Khomh.

### Abstract
Deep learning has made remarkable progress in various sectors in recent years, significantly impacting people's daily lives. It has revolutionized healthcare, autonomous vehicles, and cybersecurity. However, like typical software systems, deep learning systems are susceptible to bugs, some of which can have a severe impact, as evidenced by fatal incidents involving Tesla's Autopilot technology. Despite the substantial advancements in deep learning techniques, little research has focused on the problem of reproducing bugs in these systems. This lack of attention is concerning, as non-reproducible bugs can hinder bug-fixing. Existing literature suggests that only 3% of machine learning and deep learning bugs are reproducible, underscoring the need for further research to tackle this issue. In this project, we thus conduct an empirical study focusing on the reproducibility of bugs in deep learning systems. Firstly, we constructed a dataset of different types of deep-learning bugs from Stack Overflow posts. This dataset comprises 123 Model, 204 Tensor, 103 Training, 110 GPU and 28 API Bugs. Secondly, we determined the reproducibility status of these bugs (e.g., reproducible, non-reproducible) by attempting to reproduce them using the bug descriptions, source code, and complementary information. During reproduction, we identify editing actions that can reproduce deep learning bugs and the critical information in bug reports that makes these bugs reproducible. Finally, we identify the edit actions required for reproducing specific types of deep learning bugs using the Apriori algorithm. In this paper, we successfully reproduce 85 deep learning bugs and identify 10 edit actions that can be used to reproduce the deep learning bugs. Furthermore, we identify the critical edit operations for different categories of deep learning bugs and the critical information in bug reports which helps the reproducibility of these bugs. Thus, our findings offer important insights for future research targeting the reproducibility of bugs in deep learning systems.

### Materials Included
* Analysis Folder: This folder contains Jupyter notebooks focused on dataset analysis. The notebooks include code for implementing the Apriori algorithm, which is used to identify critical edit actions. These actions are essential for gathering the necessary information required to reproduce bugs.
* Dataset Folder: Within this directory, you'll find various datasets, including those for PyTorch, TensorFlow (TF), and Keras Posts. The folder also contains queries used to filter the data and retrieve specific posts. Additionally, reproducibility results are included, along with corresponding edit actions and vital bug report details.
* Bugs Folder In this folder, a collection of bugs is organized, alongside their original code snippets sourced from Stack Overflow. Completed code snippets associated with each bug are also provided. Each specific bug folder contains the following elements:
  - `main.py`: Finalized code snippet.
  - `original_code_snippet.py`: Original code snippet from Stack Overflow.
  - Output files: Logs containing output information.
  - `requirements.txt` file is generated to facilitate the installation of necessary dependencies for each specific bug.

### System Requirements
- **Operating System:** Windows 10 or higher
- **Python Version:** 3.10
- **Disk Space:** ~3.5 GB
- **Development Environment:** Visual Studio Code (VS Code)
- **RAM:** 16GB
- **GPU:** N/A

### Installation Instructions

To replicate the work, follow these steps:

#### Step 1: Setting Up the Virtual Environment
1. Create a virtual environment using the following command:
    ```shell
    python -m venv venv
    ```

##### Step 2: Installing Dependencies
1. After creating the virtual environment, activate it by following the instructions [here](https://docs.python.org/3/library/venv.html).
2. Install the necessary dependencies for the required bug:
    ```shell
    cd Bugs/<BugID>
    pip install -r requirements.txt
    ```
###  Bug Reproduction
After installing the dependencies, run the following command to reproduce the bug
```shell
python main.py &> output.txt
```
This ensures that the code to reproduce the bug is run and the results are stored in the output file. To check the original bug report, go to the `BugReproducibility_FSE24.xlsx` and find the Stack Overflow Post of the corresponding Bug ID. This will help you verify the output of the reproduced bug and the original error message.


### Bug Reproduction - All Bugs
To reproduce all the bugs, download the data and dependencies for the bugs, and run the following command.
```shell
cd Bugs
python script.py
```

### Analysis
To analyze the results, and run the code for Apriori implementation, go to the respective Jupyter notebook in the Analysis folder and run the cells in the notebook sequentially.

### Licensing Information
This project is licensed under the MIT License, a permissive open-source license that allows others to use, modify, and distribute the project's code with very few restrictions. This license can benefit research by promoting collaboration and encouraging the sharing of ideas and knowledge. With this license, researchers can build on existing code to create new tools, experiments, or projects, and easily adapt and customize the code to suit their specific research needs without worrying about legal implications. The open-source nature of the MIT License can help foster a collaborative research community, leading to faster innovation and progress in their respective fields. Additionally, the license can help increase the visibility and adoption of the project, attracting more researchers to use and contribute to it.

### Acknowledgment & References

During the implementation of our study, we have referred to the following papers:

Papers:
1. Mondal et al., “Can Issues Reported at Stack Overflow Questions be Reproduced? An Exploratory Study”, MSR19
2. Rahman et al., “Why are Some Bugs Non-Reproducible?: An Empirical Investigation using Data Fusion”, ICSME20
4. Moravati et al., “Bugs in machine learning-based systems: a faultload benchmark”, EMSE23
