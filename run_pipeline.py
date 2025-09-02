import subprocess
import sys

def run_pipeline():
    print("🚀 Iniciando pipeline completo...")
    
    try:
        # 1. Coleta de dados
        print("📰 Etapa 1: Coletando notícias...")
        subprocess.run([sys.executable, "src/data_collection.py"], check=True)
        
        # 2. Processamento
        print("⚙️ Etapa 2: Processando dados...")
        subprocess.run([sys.executable, "src/data_processing.py"], check=True)
        
        print("✅ Pipeline concluído com sucesso!")
        print("🎯 Execute: streamlit run app.py para ver o dashboard")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no pipeline: {e}")

if __name__ == "__main__":
    run_pipeline()