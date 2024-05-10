import pip
import os
import mlflow
from mlflow.types.schema import Schema, ColSpec
from mlflow.models import ModelSignature
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SabIAQueryModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        logging.info("Starting to load the model context.")

       
        os.environ["CUDACXX"] = "/usr/local/cuda-12/bin/nvcc"
        os.environ["CMAKE_ARGS"] = "-DLLAMA_CUBLAS=on"
        os.environ["FORCE_CMAKE"] = "1"
        
        pip.main(["install", "llama-cpp-python==0.2.55"])
        pip.main(["install", "langchain"])
        pip.main(["install", "tiktoken"])
        pip.main(["install", "chromadb"])
        pip.main(["install", "PyMuPDF"])
        logging.info("Installed dependencies.")
       
        from src.tokenizers.sabia_tokenizer import SabIATokenizer
        from src.models.sabia_embeddings_model import SabIAEmbeddingsModel
        from src.vectordbs.chroma_vectordb import ChromaVectorDB
        from src.chains.demo_loader_chain import DemoLoaderChain
        from framework_classes.memory import Memory
        from src.models.demo_model import DemoModel
        from src.prompt_templates.demo_prompt_template import DemoPromptTemplate
        from src.prompts.demo_prompt import DemoPrompt
        
        logging.info("Initialized components.")
      
        logging.info("Starting the document upload chain.")
        full_model_path = os.path.join(context.artifacts["models"], "ggml-model-f16-Q5_K_M.gguf")
        self.tokenizer = SabIATokenizer()
        self.embedding = SabIAEmbeddingsModel(model_path=full_model_path, tokenizer=self.tokenizer, n_gpu_layers=32)
        self.vectordb = ChromaVectorDB(embedding_model=self.embedding)
        self.llm_model = DemoModel(model_path=full_model_path, n_gpu_layers=32, stop_tags=["</answer>"])
        self.prompt = DemoPrompt(DemoPromptTemplate(), self.vectordb)
        self.memory = Memory(20)

        
        DemoLoaderChain(self.vectordb, self.tokenizer, docs_paths=[context.artifacts["docs"] + "/AIStudioDoc.pdf"]).run()
        logging.info("Document upload chain completed.")
        
    def predict(self, context, model_input):
        logging.info("Document upload chain completed.")
        from framework_classes.message import Message
        user_input = model_input['question'][0]
        message = Message("User", user_input)
        self.memory.add_message(message)
        history = self.memory.get_history()
        content, chunks = self.prompt.get_prompt(message, history)
        answer = self.llm_model.predict(content) + " "
        start = answer.index("Answer: <answer>") + 16
        answer = answer[start:answer.find("User", start)].strip()
        self.memory.add_message(Message("Assistant", answer))
        logging.info("Prediction completed.")
        return {
            "chunks": [x.content for x in chunks],
            "history": [f"<{x.role}> {x.content} \n" for x in history],
            "prompt": content,
            "output": answer
        }

    @classmethod
    def log_model(cls, model_folder, docs_folder, demo_folder):
        input_schema = Schema([ColSpec("string", "question")])
        output_schema = Schema([
            ColSpec("string", "chunks"),
            ColSpec("string", "history"),
            ColSpec("string", "prompt"),
            ColSpec("string", "output")
        ])
        signature = ModelSignature(inputs=input_schema, outputs=output_schema)
        artifacts = {"models": model_folder, "docs": docs_folder, "demo": demo_folder}

        mlflow.pyfunc.log_model(
            artifact_path="sabia_artifacts",
            python_model=cls(),
            artifacts=artifacts,
            signature=signature,
            pip_requirements=["mlflow", "langchain", "tiktoken", "chromadb", "PyMuPDF", "llama-cpp-python==0.2.55"],
            code_path=["src", "framework_classes"]
        )

if __name__ == "__main__":
    logging.info("Configuring experiment in MLflow.")
    mlflow.set_experiment(experiment_name='SabIA')
    with mlflow.start_run(run_name='RAG_with_5b_quantization') as run:
        SabIAQueryModel.log_model(
            model_folder='/home/jovyan/datafabric/Llama7b',
            docs_folder="docs",
            demo_folder="demo"
        )
        mlflow.register_model(
            model_uri=f"runs:/{run.info.run_id}/sabia_artifacts", 
            name="RAG_with_5b_quantization"
        )
        print(f"Model registered with run ID: {run.info.run_id}")
    logging.info("Model registered successfully.")
