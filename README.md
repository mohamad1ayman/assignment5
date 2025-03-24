# assignment5
# Blog Content Repurposer

This project provides a system for repurposing blog content into multiple formats such as summaries, social media posts, and newsletters using AI-powered strategies.

## Setup Instructions

### Prerequisites
Before running the script, ensure you have the following installed:
- Python 3.8 or later
- pip (Python package manager)

### Installation Steps

1. **Clone the Repository**
   ```sh
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create and Activate a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add your API keys:
   ```sh
   MODEL_SERVER=GROQ  # Change to OPTOGPT, NGU, or OPENAI as needed
   GROQ_API_KEY=your_groq_api_key
   GROQ_BASE_URL=your_groq_base_url
   GROQ_MODEL=your_groq_model
   OPTOGPT_API_KEY=your_optogpt_api_key
   OPTOGPT_BASE_URL=your_optogpt_base_url
   OPTOGPT_MODEL=your_optogpt_model
   NGU_API_KEY=your_ngu_api_key
   NGU_BASE_URL=your_ngu_base_url
   NGU_MODEL=your_ngu_model
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_MODEL=gpt-4
   ```

5. **Run the Script**
   ```sh
   python script.py
   ```

## Usage
To use the blog content repurposer, modify the `sample_blog_post` variable with your blog content and execute the script. The script will generate:
- A summary
- Social media posts for Twitter, LinkedIn, and Facebook
- An email newsletter

## License
This project is licensed under the MIT License. Feel free to modify and distribute as needed.

## Contributing
If you would like to contribute, please fork the repository and submit a pull request.

## Contact
For questions or support, reach out via GitHub Issues.

