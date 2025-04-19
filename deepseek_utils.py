import os
import requests
import pandas as pd
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def query_deepseek(
    df: pd.DataFrame,
    custom_prompt: Optional[str] = None,
    temperature: float = 0.3
) -> str:
    """
    Get AI analysis of PCB risk data
    
    Args:
        df: Processed DataFrame with risk calculations
        custom_prompt: Optional override for default prompt
        temperature: AI creativity (0-1)
    
    Returns:
        Analysis text
    """
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY missing from environment")

    try:
        # Prepare data summary
        stats = {
            "total_samples": len(df),
            "risk_distribution": df['Status'].value_counts().to_dict(),
            "top_risky": df.nlargest(3, 'Total_PCB').to_dict('records')
        }

        # Default prompt
        prompt = custom_prompt or f"""
        As a toxicology expert, analyze this PCB exposure data:
        {stats}
        
        Provide:
        1. Overall risk assessment
        2. Notable high-risk cases
        3. Recommended actions
        4. Data quality observations
        """

        # API request
        response = requests.post(
            DEEPSEEK_API_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an environmental health expert analyzing PCB exposure data."
                    },
                    {
                        "role": "user",
                        "content": prompt.strip()
                    }
                ],
                "temperature": temperature,
                "max_tokens": 1000
            },
            timeout=30
        )
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected API response: {str(e)}")