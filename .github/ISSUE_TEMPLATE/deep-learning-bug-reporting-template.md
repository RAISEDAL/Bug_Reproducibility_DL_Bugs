# Deep Learning Bug Reporting Guidelines

To ensure efficient bug reporting and faster resolution, please follow these guidelines when reporting a bug in your deep learning setup:

## Configuration Information

Please provide the following details about your deep learning setup:

-   **Framework:** State the deep learning framework you use, such as TensorFlow, PyTorch, Keras, etc.
-   **Libraries:** List any additional libraries you have imported for your project.
-   **Dependency Information:** Include versions of the deep learning framework and other libraries. You can obtain this information by running the command `pip list` in your default environment.
-   **Hardware Dependencies (if any):** Specify any specific hardware dependencies you utilize, such as GPUs, TPUs, or other accelerators.

## Dataset Information

To gain better insight into the bug, provide the following information about your dataset:

-   **Data Shape:** State the dimensions of your dataset, including the number of samples and features.
-   **Number of Categorical & Numerical Columns:** Mention the count of categorical and numerical columns in your dataset.
-   **Categories in Categorical Columns:** If you have categorical data, provide the unique levels or categories in that column.
-   **Distribution of Numerical Columns:** If you have numerical data, describe the distribution (e.g., mean, standard deviation, range) to help identify potential outliers or anomalies.
-   **Preprocessing Operations (if any):** Specify any preprocessing steps you applied to the dataset, such as normalization, scaling, feature engineering, or handling missing values.

## Neural Network Information

To better understand the bug, include the following information about your neural network architecture:

-   **Type of Layers:** Describe the layers used in your neural network (e.g., Dense, Convolutional, Recurrent, etc.).
-   **Number of Layers:** Mention your neural network's total number of layers.
-   **Activation Function:** State the activation functions used in the network.
-   **Architecture:** Provide a concise description of the neural network's architecture, including the input and output dimensions.

It would be beneficial if you could provide the code snippet for your model.

## Hyperparameters

Include the following information about your neural network's hyperparameters:

-   **Batch Size:** Specify the batch size used during training.
-   **Epochs:** Mention the number of epochs used in training.
-   **Optimizer:** State the optimizer used during training.
-   **Loss Function:** Specify the loss function used in the network.
-   **Custom Implementations of Hyperparameters:** If you have used custom implementations for hyperparameters (e.g., a custom loss function), please provide relevant details.

## Logs

Please include the following logs:

-   **Training Logs:** Include all relevant information and errors encountered during training. This includes the loss at each epoch, loss at each step, and any other relevant metrics computed during training.
-   **Evaluation Logs:** Include the results and metrics from evaluating the trained model on a separate validation or test dataset.
-   **Compiler Error Logs:** If you encountered any errors during code compilation or execution, please provide the specific error messages and relevant parts of the code where the errors occurred.

Additionally, to facilitate the bug investigation and help us reproduce your issue, please consider including a minimal reproducible example (MRE) of your code. A [MRE](https://stackoverflow.com/help/minimal-reproducible-example) is a simplified version of your deep learning setup that demonstrates the problem you encountered. By providing an MRE, our team can quickly isolate and understand the bug, leading to faster resolution.

When creating the MRE, focus on including only the essential components needed to reproduce the issue. Remove any unnecessary code or data that does not contribute to the bug. This will ensure that the problem is clear and easy to analyze.

Please include the MRE and the other relevant information mentioned in the guidelines above. Your cooperation in providing a minimal reproducible example will greatly assist our efforts in resolving the bug. Thank you!
