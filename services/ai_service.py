import google.generativeai as genai
import os

# Use old library syntax
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_with_gemini(resume_text, github_data):
    """
    Generates a consolidated HTML Report.
    """
    model = genai.GenerativeModel('models/gemini-flash-latest')
    
    prompt = f"""
    ROLE: Senior Technical Auditor.
    TASK: Verify Candidate Claims vs GitHub Evidence.

    INPUT DATA:
    1. RESUME SUMMARY: {resume_text[:15000]}
    2. GITHUB DEEP SCAN: {github_data}

    INSTRUCTIONS:
    - Analyze the 'detected_tech' and 'languages' keys in GitHub Data.
    - Create a SINGLE table for ALL skills (Languages, DBs, Frameworks).
    - If a skill is in Resume but NOT in GitHub -> Mark as GHOST.
    - If a skill is found in GitHub -> Mark as VERIFIED.
    - "Confidence" should be High if verified by code/dependencies, Low if only text match.

    OUTPUT FORMAT:
    Return ONLY raw HTML. Use Bootstrap 5 classes.
    Structure:

    <div class="card shadow-sm mb-4">
        <div class="card-header bg-primary text-white d-flex justify-content-between">
            <h4 class="mb-0">🛡️ Technical Audit Report</h4>
            <span>Verified: [X]%</span>
        </div>
        
        <div class="card-body">
            <div class="alert alert-light border-start border-4 border-primary">
                <strong>Verdict:</strong> [2 sentence professional summary of candidate authenticity]
            </div>

            <h5 class="mt-4 mb-3">🔬 Skill Verification Matrix</h5>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead class="table-light">
                        <tr>
                            <th style="width: 25%">Skill Claimed</th>
                            <th style="width: 15%">Status</th>
                            <th style="width: 45%">Evidence (Repo/File)</th>
                            <th style="width: 15%">Confidence</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>[Skill Name]</strong></td>
                            <td>
                                <span class="badge bg-success">Verified</span> 
                            </td>
                            <td>Found in <code>[Repo Name]</code> (via [File])</td>
                            <td>High</td>
                        </tr>
                        <tr>
                            <td><strong>[Missing Skill]</strong></td>
                            <td><span class="badge bg-danger">Ghost</span></td>
                            <td>No evidence in 15 repos scanned</td>
                            <td>Low</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="row mt-4">
                <div class="col-md-6">
                    <h6 class="text-success">💎 Hidden Strengths</h6>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">
                            [Skill found in GitHub but not in Resume]
                            <br><small class="text-muted">Used in [Repo Name]</small>
                        </li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h6 class="text-dark">👨‍💻 Coding Habits</h6>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">
                            <strong>Consistency:</strong> [Active/Sporadic]
                        </li>
                        <li class="list-group-item">
                            <strong>Documentation:</strong> [Good/Poor] READMEs
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.replace("```html", "").replace("```", "")
    except Exception as e:
        return f"<div class='alert alert-danger'>AI Error: {str(e)}</div>"