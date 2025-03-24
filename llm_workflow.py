import os
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import importlib.util
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the model server type
model_server = os.getenv('MODEL_SERVER', 'GROQ').upper()  # Default to GROQ if not set

if model_server == "OPTOGPT":
    API_KEY = os.getenv('OPTOGPT_API_KEY')
    BASE_URL = os.getenv('OPTOGPT_BASE_URL')
    LLM_MODEL = os.getenv('OPTOGPT_MODEL')

elif model_server == "GROQ":
    API_KEY = os.getenv('GROQ_API_KEY')
    BASE_URL = os.getenv('GROQ_BASE_URL')
    LLM_MODEL = os.getenv('GROQ_MODEL')

elif model_server == "NGU":
    API_KEY = os.getenv('NGU_API_KEY')
    BASE_URL = os.getenv('NGU_BASE_URL')
    LLM_MODEL = os.getenv('NGU_MODEL')

elif model_server == "OPENAI":
    API_KEY = os.getenv('OPENAI_API_KEY')
    BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')  # Default to OpenAI's standard base URL
    LLM_MODEL = os.getenv('OPENAI_MODEL')

else:
    raise ValueError(f"Unsupported MODEL_SERVER: {model_server}")

# Initialize the OpenAI client with custom base URL
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# Dynamic LLM Client Loader
class LLMClientLoader:
    """
    Dynamically load and configure LLM clients based on environment variables.
    Supports pluggable LLM providers with a consistent interface.
    """
    @staticmethod
    def load_client():
        global client
        return client

@dataclass
class ContentStrategy:
    """Base strategy for content generation with fallback mechanisms."""
    
    def generate(self, context: Dict[str, str]) -> str:
        """
        Generate content with LLM and fallback to rule-based method.
        
        Args:
            context: Dictionary containing content generation context
        
        Returns:
            Generated content string
        """
        try:
            # Attempt LLM-powered generation
            llm_result = self._llm_generate(context)
            return llm_result if llm_result else self._rule_generate(context)
        except Exception:
            # Fallback to rule-based method
            return self._rule_generate(context)
    
    def _llm_generate(self, context: Dict[str, str]) -> Optional[str]:
        """LLM-powered content generation (to be implemented by subclasses)."""
        raise NotImplementedError
    
    def _rule_generate(self, context: Dict[str, str]) -> str:
        """Rule-based content generation (to be implemented by subclasses)."""
        raise NotImplementedError

class SummaryStrategy(ContentStrategy):
    def _llm_generate(self, context: Dict[str, str]) -> Optional[str]:
        """Generate summary using LLM."""
        client = LLMClientLoader.load_client()
        messages = [
            {"role": "system", "content": "Create a concise blog summary."},
            {"role": "user", "content": f"Summarize this blog post: {context['blog_post']}"}
        ]
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            max_tokens=250
        )
        
        return response.choices[0].message.content.strip()
    
    def _rule_generate(self, context: Dict[str, str]) -> str:
        """Fallback summary generation using basic text extraction."""
        blog_post = context['blog_post']
        paragraphs = blog_post.split('\n\n')
        
        # Take first two paragraphs and truncate
        summary = ' '.join(paragraphs[:2])
        return summary[:250] + '...' if len(summary) > 250 else summary

class SocialMediaStrategy(ContentStrategy):
    def _llm_generate(self, context: Dict[str, str]) -> Optional[str]:
        """Generate social media posts using LLM."""
        client = LLMClientLoader.load_client()
        messages = [
            {"role": "system", "content": "Create engaging social media posts."},
            {"role": "user", "content": f"Create social posts for: {context['title']}"}
        ]
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages
        )
        
        return response.choices[0].message.content.strip()
    
    def _rule_generate(self, context: Dict[str, str]) -> str:
        """Fallback social media post generation."""
        title = context['title']
        hashtags = ' '.join(['#' + word.lower() for word in title.split() if len(word) > 3])
        return f"{title}\n\nRead more: [LINK]\n\n{hashtags}"

class NewsletterStrategy(ContentStrategy):
    def _llm_generate(self, context: Dict[str, str]) -> Optional[str]:
        """Generate newsletter using LLM."""
        client = LLMClientLoader.load_client()
        messages = [
            {"role": "system", "content": "Create an engaging email newsletter."},
            {"role": "user", "content": f"Create newsletter for blog: {context['blog_post']}"}
        ]
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages
        )
        
        return response.choices[0].message.content.strip()
    
    def _rule_generate(self, context: Dict[str, str]) -> str:
        """Fallback newsletter generation."""
        title = context['title']
        paragraphs = context['blog_post'].split('\n\n')
        
        newsletter = f"""
Subject: {title}

Hi there!

Check out our latest blog post: {title}

Highlights:
{paragraphs[1] if len(paragraphs) > 1 else ''}

Read full article: [LINK]

Cheers!
"""
        return newsletter

@dataclass
class BlogContentRepurposer:
    """Comprehensive blog content repurposing system."""
    
    blog_post: str
    title: str = field(init=False)
    sections: Dict[str, str] = field(init=False)
    
    def __post_init__(self):
        """Initialize title and sections during object creation."""
        self.title = self._extract_title()
        self.sections = self._extract_sections()
    
    def _extract_title(self) -> str:
        """Extract blog post title."""
        lines = self.blog_post.split('\n')
        title_lines = [line for line in lines if line.startswith('# ')]
        return title_lines[0].lstrip('# ').strip() if title_lines else "Untitled Blog Post"
    
    def _extract_sections(self) -> Dict[str, str]:
        """Extract sections from blog post."""
        sections = {}
        current_section = "Introduction"
        lines = self.blog_post.split('\n')
        
        section_content = []
        for line in lines:
            if line.startswith('## '):
                if current_section != "Introduction":
                    sections[current_section] = '\n'.join(section_content).strip()
                current_section = line.lstrip('# ').strip()
                section_content = []
            else:
                section_content.append(line)
        
        # Add last section
        if section_content:
            sections[current_section] = '\n'.join(section_content).strip()
        
        return sections
    
    def repurpose(self) -> Dict:
        """Repurpose blog content using different strategies."""
        context = {
            'blog_post': self.blog_post,
            'title': self.title,
            'sections': self.sections
        }
        
        return {
            'title': self.title,
            'summary': SummaryStrategy().generate(context),
            'social_media_posts': {
                'twitter': SocialMediaStrategy().generate(context),
                'linkedin': SocialMediaStrategy().generate(context),
                'facebook': SocialMediaStrategy().generate(context)
            },
            'email_newsletter': NewsletterStrategy().generate(context)
        }

def repurpose_blog_content(blog_post: str) -> Dict:
    """Main function to repurpose blog content."""
    repurposer = BlogContentRepurposer(blog_post)
    return repurposer.repurpose()

# Example usage
if __name__ == "__main__":
    sample_blog_post = """# The Future of Artificial Intelligence in Healthcare
    
## Introduction

Artificial intelligence (AI) is revolutionizing the healthcare industry, offering innovative solutions to long-standing challenges. From diagnostics to treatment plans, AI technologies are being integrated into various aspects of healthcare delivery. These advancements promise to improve patient outcomes, reduce costs, and enhance operational efficiency.

The rapid development of machine learning algorithms, coupled with the increasing availability of healthcare data, has created unprecedented opportunities for AI applications in medicine. Healthcare providers, researchers, and technology companies are collaborating to harness this potential.

## Diagnostic Applications

One of the most promising applications of AI in healthcare is in diagnostics. Machine learning algorithms can analyze medical images such as X-rays, MRIs, and CT scans with remarkable accuracy. In some cases, AI systems have demonstrated the ability to detect conditions like cancer at earlier stages than human radiologists.

Computer vision technologies can identify subtle patterns that might be missed by the human eye. For example, AI systems can detect minute changes in skin lesions that could indicate melanoma, potentially saving lives through early intervention.

## Treatment Planning

AI is also transforming treatment planning by analyzing vast amounts of patient data to recommend personalized treatment options. These systems can consider a patient's medical history, genetic information, lifestyle factors, and responses to previous treatments.

By processing this comprehensive data, AI can help clinicians develop more effective treatment plans. This is particularly valuable in complex cases where multiple treatment options exist, or when standard approaches have been unsuccessful.

## Conclusion

The future of AI in healthcare is bright, with potential benefits for patients, providers, and healthcare systems. As technology continues to evolve, collaboration between technologists, healthcare professionals, ethicists, and policymakers will be essential to realize the full potential of AI while mitigating risks.
"""
    
    results = repurpose_blog_content(sample_blog_post)
    
    print(f"Title: {results['title']}\n")
    print(f"Summary:\n{results['summary']}\n")
    print("Social Media Posts:")
    for platform, post in results['social_media_posts'].items():
        print(f"\n{platform.upper()}:")
        print(post)
    print(f"\nEmail Newsletter:\n{results['email_newsletter']}")