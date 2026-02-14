from groq import Groq
from app.config import settings

client = Groq(
    api_key = settings.GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are ResumeCritic, an expert resume reviewer with 15+ years of experience in technical recruiting.
Your specialty is providing brutally honest, actionable feedback that helps candidates dramatically improve their resumes.
You've reviewed over 10,000 resumes and have deep knowledge of what makes top candidates stand out.

Key principles:
- Be specific: always quote actual text from the resume
- Be actionable: every critique should come with a fix
- Be honest: call out fluff, buzzwords, and lazy writing
- Be fair: recognize genuine strengths when present
- Be strategic: focus on high-impact changes first

You understand the difference between junior and senior resumes, and you calibrate your feedback accordingly.
"""

RESUME_ROAST_PROMPT = """
    You are a brutally honest resume critic with 15+ years of experience in tech recruiting and talent acquisition.
    Your job is to roast this resume while providing actionable feedback that will genuinely help the candidate improve.

    **Resume Text:**
    {resume_text}

    **Instructions:**
    Provide a comprehensive roast covering these areas:

    1. **First Impressions (The "3-Second Test")**
    - Does this resume pass the recruiter's initial glance?
    - What immediately stands out (good or bad)?
    - Is the formatting helping or hurting?

    2. **Content Quality**
    - Are accomplishments quantified with metrics and impact?
    - Is there fluff, buzzwords, or meaningless jargon?
    - Are bullet points achievement-focused or just listing duties?
    - Does it show progression and growth?

    3. **Technical Red Flags**
    - Skills section: credible or kitchen sink?
    - Are claimed skills backed up by actual experience?
    - Any outdated technologies that should be removed?
    - Missing critical skills for the apparent target role?

    4. **Writing & Communication**
    - Clarity and conciseness
    - Grammar, spelling, consistency
    - Active voice vs passive voice
    - Unnecessary words or redundancy

    5. **Strategic Positioning**
    - Is there a clear narrative/career story?
    - Does it target a specific role or is it generic?
    - What's missing that would make this candidate stand out?

    6. **The Brutal Truth**
    - What would make you immediately reject this resume?
    - What specific changes would move this from "pass" to "interview"?

    **Tone:** Be direct and honest, but constructive. Use humor where appropriate, but the goal is improvement, not just entertainment. Call out BS, but also recognize genuine strengths.

    **Format:** 
    - Start with a TL;DR verdict (Interview/Maybe/Pass and why)
    - Use specific examples from the resume
    - End with 3-5 highest-impact changes to make immediately

    **Output:**
    Provide your roast now.
"""

RESUME_ROAST_PROMPT_STRUCTURED = """
    You are an expert resume reviewer conducting a thorough critique of the following resume.

    **Resume Text:**
    {resume_text}

    **Target Role (if known):** {target_role}

    Analyze this resume and provide feedback in the following JSON structure:

    {{
    "overall_verdict": {{
        "rating": "strong_yes|yes|maybe|no|strong_no",
        "tldr": "One sentence summary of your verdict",
        "would_interview": true/false
    }},
    "strengths": [
        {{
        "category": "formatting|content|experience|skills|impact",
        "observation": "Specific strength",
        "example": "Quote or reference from resume"
        }}
    ],
    "weaknesses": [
        {{
        "category": "formatting|content|experience|skills|impact|grammar",
        "severity": "critical|high|medium|low",
        "issue": "Specific problem",
        "example": "Quote or reference from resume",
        "fix": "How to fix this"
        }}
    ],
    "red_flags": [
        "List of anything that would immediately disqualify or raise concerns"
    ],
    "missing_elements": [
        "Critical things that should be present but aren't"
    ],
    "top_3_changes": [
        {{
        "priority": 1-3,
        "change": "Specific actionable change",
        "impact": "Why this matters",
        "example": "Before/after if applicable"
        }}
    ],
    "roast": {{
        "opening": "Your brutally honest first reaction",
        "key_critiques": ["3-5 specific roasts with examples"],
        "closing": "Final verdict with motivation"
    }}
    }}

    Be specific, quote actual text from the resume, and focus on high-impact feedback.
"""

def get_roast_prompt(resume_text: str, style: str = "balanced", target_role: str = None):
    """
    Generate a resume roast prompt with different styles.

    Args:
        resume_text: The resume text to roast
        style: 'gentle', 'balanced', 'brutal'
        target_role: Optional target role for context

    Returns:
        Formatted prompt string
    """

    tone_instructions = {
        "gentle": """
                Be constructive and encouraging. Focus on actionable improvements while acknowledging strengths.
                Assume the candidate is early career or making a career transition.
                """,

        "balanced": """
                Be direct and honest while remaining professional. Point out both strengths and weaknesses clearly. 
                This is for someone who wants real feedback, not sugar-coating.
                """,

        "brutal": """
                Be ruthlessly honest. This candidate specifically asked for a harsh critique. Don't hold back on 
                calling out BS, fluff, or lazy resume writing. Use humor, but make every critique count. 
                This should sting a little but ultimately help them improve significantly.
                """
    }

    prompt = f"""
    You are an expert resume critic with deep experience in hiring for technical roles.

    **Resume Text:**
    {resume_text}

    {f"**Target Role:** {target_role}" if target_role else ""}

    **Style:** {tone_instructions[style]}

    **Analysis Framework:**

    1. **First Impression** (3-second recruiter test)
    - Visual layout and readability
    - Immediate strengths or red flags
    
    2. **Content Analysis**
    - Quantified achievements vs. responsibility lists
    - Buzzword density and authenticity
    - Career progression narrative
    - Skills credibility (claimed vs. demonstrated)

    3. **Writing Quality**
    - Clarity and conciseness
    - Grammar and consistency
    - Action verbs and impact language

    4. **Strategic Gaps**
    - Missing critical information
    - Weak positioning for target roles
    - Opportunities to differentiate

    5. **The Roast**
    - Specific examples of what's not working
    - Why a recruiter might pass on this resume
    - Top 3 changes for maximum impact

    **Output Format:**
    - TL;DR verdict with rating
    - Detailed analysis with specific examples
    - Actionable improvements prioritized by impact
    - Final motivation/encouragement

    Begin your roast:
    """
    return prompt

def roast_resume(resume_text: str, style: str = "balanced", target_role: str = None):
    """
    Main function to roast a resume.
    """
    roast_prompt = get_roast_prompt(resume_text, style, target_role)

    chat_completion = client.chat.completions.create(
    messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": roast_prompt,
            }
        ],
        model=settings.LLM_MODEL
    )

    return chat_completion.choices[0].message.content
