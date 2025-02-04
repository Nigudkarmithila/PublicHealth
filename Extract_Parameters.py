import PyPDF2
import re

# 1. The PARAMETERS dictionary
PARAMETERS = {
    "Study Design": [
        "study design", "methodology", "randomized controlled trial",
        "cross-sectional", "observational", "longitudinal"
    ],
    "Population": [
        "sample size", "participants", "demographics", "age", "gender",
        "education", "employment", "location"
    ],
    "Health Condition": [
        "health condition", "disease", "disorder", "depression", "anxiety",
        "stress", "psychotic", "schizophrenia"
    ],
    "Intervention Type": [
        "treatment", "intervention", "medication", "therapy", "herbal",
        "digital intervention", "smartphone app", "prescription"
    ],
    "Control Group": [
        "control group", "placebo", "alternative treatment", "standard treatment"
    ],
    "Outcome Measures": [
        "outcome measure", "scale", "assessment", "evaluation", "PHQ-9",
        "HAMA", "GAD-7", "HAMD", "adherence"
    ],
    "Duration": [
        "duration", "follow-up period", "weeks", "months", "years"
    ],
    "Efficacy": [
        "efficacy", "effectiveness", "symptom reduction", "clinical significance"
    ],
    "Adverse Events": [
        "side effects", "adverse effects", "tolerance", "drug interaction",
        "medication response"
    ],
    "Cultural and Socioeconomic Factors": [
        "cultural beliefs", "stigma", "financial barriers", "social support"
    ],
    "Data Collection Methods": [
        "data collection", "survey", "self-report", "clinical assessment"
    ],
    "Statistical Analysis": [
        "statistical analysis", "regression model", "chi-square test",
        "t-test", "mixed modeling"
    ],
    "Engagement/Adherence": [
        "adherence", "compliance", "dropout rate", "user engagement"
    ],
    "Comparison with Standard Treatments": [
        "comparison", "benchmark", "standard medication", "alternative treatment"
    ],
    "Mode of Delivery": [
        "mode of delivery", "digital", "mobile app", "medication", "infusion"
    ],
    "Key Findings": [
        "conclusion", "findings", "results", "summary"
    ]
}

def read_pdf(pdf_file_path: str) -> str:
    """
    Reads a PDF file and returns all text content as a single string.
    Uses PyPDF2 for text extraction. 
    """
    text_content = []
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
    return "\n".join(text_content)

def extract_parameters_from_text(text: str, parameters_dict: dict) -> dict:
    """
    For each category in parameters_dict, find any line of text that 
    contains a keyword from that category. Return a dictionary mapping
    from category -> list of matched lines.
    
    - text: the full PDF text
    - parameters_dict: a dictionary of {ParameterName: [keyword1, keyword2, ...]}
    """
    # Split text into lines to store where the keywords appear
    lines = text.split("\n")

    # Prepare a result dict with the same keys as parameters_dict
    extracted_info = {param: [] for param in parameters_dict.keys()}

    # For each line, check each parameter’s keyword list
    for line in lines:
        line_lower = line.lower()
        for param, keywords in parameters_dict.items():
            for kw in keywords:
                # If keyword is found in the line (case-insensitive):
                if kw.lower() in line_lower:
                    extracted_info[param].append(line.strip())
                    # Optionally, break here if you only want to add the line once
                    # for the first matching keyword. But some lines may contain multiple 
                    # relevant keywords. So you might skip breaking to capture all relevant 
                    # parameter matches in the same line.
                    break

    return extracted_info


if __name__ == "__main__":
    # 1. Path to your PDF
    pdf_path = "smartphoneapp_rct.pdf"

    # 2. Extract the text from the PDF
    text_data = read_pdf(pdf_path)

    # 3. Extract lines relevant to each parameter
    extraction_results = extract_parameters_from_text(text_data, PARAMETERS)

    # 4. Print out the results in a readable way
    for param, lines in extraction_results.items():
        print(f"=== {param} ===")
        if lines:
            for i, l in enumerate(lines, start=1):
                print(f"{i}. {l}")
        else:
            print("No mention found.")
        print()