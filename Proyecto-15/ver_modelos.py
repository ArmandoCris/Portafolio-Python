import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6IuN7dSddzfr-E6oEx_ZUb98tTBFFVlB_PnDkcjGPrRcw")

print("Modelos disponibles para generar texto:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)