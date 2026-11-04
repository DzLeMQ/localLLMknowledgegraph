# 🕸️ Local LLM Knowledge Graph Construction

An automated pipeline that extracts structured entities and complex relationships from unstructured text files to dynamically build an interactive Knowledge Graph. It leverages **LangChain** and local Large Language Models (**LLMs** via Ollama) to run completely offline.

## ✨ Features
* **100% Local Execution:** Processes sensitive documents safely on your own hardware.
* **Automated Extraction:** Turns raw text files into nodes and relational edges.
* **Interactive Visualizations:** Generates a standalone HTML dynamic network graph.
* **Witcher Universe Demo:** Includes an example parsing text from *The Last Wish*.

## 🛠️ Core Technology Stack

| **Orchestration** | `LangChain` & `langchain-community` | Manages prompts, chunks text, and structures LLM outputs. |
| **Inference Engine**| `Ollama` | Runs the Large Language Model completely offline. |
| **Data Processing** | `Python 3.14+` | Coordinates text handling and execution pipelines. |
| **Graph Modeling**  | `NetworkX` | Programmatically builds, updates, and manages nodes and edges. |
| **Visualization**   | `Pyvis` | Renders the final graph into an interactive, zoomable HTML page. |
| **Environment**     | `Jupyter Notebooks` (`.ipynb`) | Provides an interactive workspace for step-by-step execution. |

## 📋 Prerequisites
* **Python:** v3.14 or higher
* **Editor:** VS Code with the **Jupyter Notebook** extension
* **Hardware:** Dedicated GPU with **12GB+ VRAM** recommended

## 🚀 Step-by-Step Installation

### 1. Set Up Your Environment
```bash
# Clone the repository
git clone https://github.com
cd localLLMknowledgegraph

# Install required dependencies
pip install langchain langchain-community networkx pyvis ollama ipykernel
```

### 2. Configure Your Local LLM (Ollama)
1. Download and install Ollama from [ollama.ai](https://ollama.ai).
2. Pull your target LLM (e.g., Llama 3 or Mistral):
   ```bash
   ollama pull llama3
   ```

## 💻 How to Run
1. Open the project in VS Code.
2. Select the `knowledge_graph.ipynb` notebook.
3. Ensure your Jupyter kernel points to your active Python environment.
4. Execute the cells sequentially to parse `the_last_wish_witch.txt` and generate your interactive graph webpage.


**Knowledge Graph Construction**

This project extracts structured entities and relationships from unstructured text to automatically build a Knowledge Graph. By leveraging Langchain and local Large Language Models (LLMs), 
the entire pipeline runs locally for maximum data privacy and zero cost-free.

**Prerequisites**
1. Python 3.14 or higher
2. VS Code with Jupyter Notebook extension (recommended)
3. 12GB+ VRAM GPU on device for running local LLMs
   
**Install local LLM**
1. Install ollama from ollama.ai
2. Pull a model using ollama command ollama pull modelname
3. Run a model using ollama coammnd ollama run modelname
4. Start chatting to test the model via prompt

**Processes Pipeline**
<p align = "center">
   <img width="529" height="419" alt="image" src="https://github.com/user-attachments/assets/0867f948-3d7d-4c7e-b4ce-81f8d236b7c7" />

</p>

<a href="https://dzlemq.github.io//localLLMknowledgegraph/last_wish_knowledge_graph">Click Here to Explore The Last Wish Knowledge Graph</a>

**Zoom In & Out to Control the View:** Use your mouse scroll wheel (or pinch/spread two fingers on a laptop trackpad) while hovering over the graph to zoom in and out.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
