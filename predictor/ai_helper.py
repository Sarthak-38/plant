import google.generativeai as genai

# ================= CONFIGURE API =================
genai.configure(api_key="AIzaSyDQBGoueL41-rv9KKMW1hf1l_chJD0noW4")

# ✅ Use new Gemini model (gemini-pro is outdated)
model = genai.GenerativeModel("gemini-1.5-flash")


# ================= GET DISEASE INFO =================
def get_disease_info(disease_name):

    # skip AI if model returns unknown
    if "Unknown" in str(disease_name):
        return "No disease information available."

    prompt = f"""
You are an agriculture expert.

Plant disease: {disease_name}

Explain in simple language:

1. What is this disease
2. Causes
3. Symptoms
4. Treatment / Cure
5. Prevention

Give short and practical answer for farmers.
"""

    try:
        response = model.generate_content(prompt)

        # handle empty response safely
        if response and hasattr(response, "text"):
            return response.text
        else:
            return "No information returned from AI."

    except Exception as e:
        return f"AI Error: {str(e)}"