# 🕸️ Local LLM Knowledge Graph Construction

An automated pipeline that extracts structured entities and complex relationships from unstructured text files to dynamically build an interactive Knowledge Graph. It leverages **LangChain** and local Large Language Models (**LLMs** via Ollama) to run completely offline.

<a href="https://dzlemq.github.io//localLLMknowledgegraph/last_wish_knowledge_graph">Click Here to Explore The Last Wish Knowledge Graph</a>

**Zoom In & Out to Control the View:** Use your mouse scroll wheel (or pinch/spread two fingers on a laptop trackpad) while hovering over the graph to zoom in and out.

## ✨ Features
* **100% Local Execution:** Processes sensitive documents safely on your own hardware.
* **Automated Extraction:** Turns raw text files into nodes and relational edges.
* **Interactive Visualizations:** Generates a standalone HTML dynamic network graph.
* **Witcher Universe Demo:** Includes an example parsing text from *The Last Wish Witch*.

## 🛠️ Core Technology Stack

* **Orchestration** | `LangChain` & `langchain-community` | Manages prompts, chunks text, and structures LLM outputs.|
* **Inference Engine**| `Ollama` | Runs the Large Language Model completely offline. |
* **Data Processing** | `Python 3.14+` | Coordinates text handling and execution pipelines. |
* **Graph Modeling**  | `NetworkX` | Programmatically builds, updates, and manages nodes and edges. |
* **Visualization**   | `Pyvis` | Renders the final graph into an interactive, zoomable HTML page. |
* **Environment**     | `Jupyter Notebooks` (`.ipynb`) | Provides an interactive workspace for step-by-step execution. |

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
