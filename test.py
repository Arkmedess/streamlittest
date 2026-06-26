from src.data.uploader import processar_csv
from src.data.supabase_client import replace_vendas

df = processar_csv("consolidado.csv")

replace_vendas(df)

print("Importação concluída")