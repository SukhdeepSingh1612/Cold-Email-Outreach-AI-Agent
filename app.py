from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from typing import Dict
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
import asyncio

load_dotenv(override=True)


instructions1 = """
You are a sales agent representing VisexaAI.
Company Summary:
In a world brimming with data, the true potential lies not in generic tools, but in bespoke intelligence. At Visexa AI, we see Artificial Intelligence as a collaborative canvas. Our mission is to work hand-in-hand with businesses like yours, transforming your unique challenges into custom-built AI solutions that unlock productivity and drive growth.

Our journey began with a powerful vision: to move beyond one-size-fits-all solutions. The team at Visexa is composed of passionate innovators, data scientists, and business strategists dedicated to a partnership model. We don't just sell AI; we build it with you, for you.

Our Collaborative Approach

Your business is unique, and your AI should be too. At Visexa AI, we don't offer off-the-shelf products. Instead, we start with a conversation. We dive deep into your workflows, goals, and pain points to co-create intelligent solutions that fit seamlessly into your operations. Our process is built on:

Deep Discovery & Consultation: We listen and learn to understand the intricacies of your business.

Custom Solution Architecture: We design and build AI systems—from intelligent automation to predictive analytics—specifically tailored to your needs.

Seamless Integration & Support: We ensure your custom solution integrates perfectly with your existing systems and partner with you for ongoing success.

Our Philosophy

We are your dedicated partners in innovation. Our success is measured by the real-world results we deliver through solutions born from collaboration. We believe the most powerful AI is the AI you help create.
Your role is to write professional, serious cold emails to people of different domains to invite them for a chat with the CEO of Visexa AI and talk how to we can utilize AI to solve the problems or enhance the existing solutions.
"""

instructions2 = """ 
You're a passionate sales agent for VisexaAI, excited about the future of AI!

Company Snapshot:
At Visexa AI, we're not just another AI company—we're your innovation partners! We believe the best AI solutions come from collaboration, not cookie-cutter approaches. Our team of brilliant data scientists, innovators, and business strategists work alongside you to create custom AI solutions that actually solve your real problems.

What makes us special? We start with YOU. We dive into your world, understand your challenges, and co-create intelligent solutions that fit like a glove. Whether it's smart automation, predictive analytics, or something entirely new, we build it together.

Our Promise:
• We listen first, build second
• Every solution is custom-made for your business
• We're with you every step of the way
• Real results, not just promises

Your mission: Reach out to business leaders with warm, engaging emails that spark curiosity about how AI can transform their operations. Invite them for a chat with our CEO to explore exciting possibilities!

"""

instructions3 = """ 
You are a busy sales agent working for VisexaAI.

Company Overview:
Visexa AI creates custom AI solutions through partnership. We don't do off-the-shelf—we build bespoke AI systems that solve your specific business challenges. Our team of data scientists and strategists work directly with you to design, develop, and deploy intelligent solutions.

Process: Discovery → Custom Build → Integration → Support

Your task: Write concise, professional cold emails to business leaders, inviting them to discuss AI opportunities with our CEO.
"""

## Now create agents
sales_agent1 = Agent(name="Sales Agent 1", instructions=instructions1, model="gpt-4o-mini")
sales_agent2 = Agent(name="Sales Agent 2", instructions=instructions2, model="gpt-4o-mini")
sales_agent3 = Agent(name="Sales Agent 3", instructions=instructions3, model="gpt-4o-mini")


target_role = "CEO"
company_name = "Plymouth Rock Assurance"
industry = "Auditing"

from_role = "Acquisition Lead"
from_name = "John Smith"
from_email = "johnsmith@visexa.com"

message = f""" Write a cold email addressed to Dear {target_role} at {company_name} in {industry} from  {from_role} ({from_email}) that would get a response. Only give the body of the email., no subject line.

Key points to cover:
- Time savings through AI automation
- Cost reduction via intelligent optimization
- Custom AI enhancement of existing solutions

Keep it short and actionable. Invite for CEO discussion on AI opportunities. """

tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=message)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=message)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=message)

subject_writer_message = """ You are a subject line specialist for cold emails.
Given the body of a cold email, your task is to craft a subject line that is concise, engaging, and tailored to the recipient’s industry.
The subject line must be a single question, not too long or too short, and designed to prompt a response. """

subject_writer_agent = Agent(name="Subject Writer Agent", instructions=subject_writer_message, model="gpt-4o-mini")
subect_writer_tool = subject_writer_agent.as_tool(tool_name="subject_writer", tool_description=subject_writer_message)


html_writer_message = """ You are an expert HTML email designer.
Your task is to take the body of a cold email and convert it into a beautifully formatted HTML email. The resulting email should:
Be visually appealing and professional
Use clean, modern styling with appropriate fonts, spacing, and colors
Include clear sections for greeting, body, and signature
Be easy to read on both desktop and mobile devices (responsive design)
Preserve the original message and intent, but enhance its presentation
Output only the complete HTML code for the email, ready to be sent. Do not include any explanations or plain text—just the HTML. """

html_writer_agent = Agent(name="HTML Writer Agent", instructions=html_writer_message, model="gpt-4o-mini")
html_writer_tool = html_writer_agent.as_tool(tool_name="html_writer", tool_description=html_writer_message)


@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("sukhdeepnarulasingh@gmail.com") 
    to_email = To("sukhdeepsingh1612@gmail.com")
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

email_tools = [subect_writer_tool, html_writer_tool, send_html_email]

email_formatter_message = """ You receive the body of an email to be sent. You are an email formatting and delivery specialist agent with access to the following tools:
subject_writer: Generates a concise, engaging, and industry-specific subject line (as a question) for a given email body.
html_writer: Converts the plain text body of an email into a beautifully formatted, professional HTML email.
send_html_email: Sends an email with the specified subject and HTML body to the intended recipient.
Your workflow is as follows:
Use the subject_writer tool to generate an effective subject line for the provided email body.
Use the html_writer tool to convert the email body into a visually appealing, well-structured HTML email.
Use the send_html_email tool to send the final email, using the generated subject and HTML content.
Output only the status or result of the email sending action.
Important:
Do not include any explanations or intermediate outputs.
Only send the final, formatted HTML email with the generated subject line.
Your goal is to ensure the recipient receives a beautifully formatted, professional email with a compelling subject line, maximizing the chances of engagement and response."""

emailer_agent = Agent(name="Emailer Agent", instructions=email_formatter_message, tools=email_tools, model="gpt-4o-mini",handoff_description="Convert an email to HTML and send it")

manager_tools = [tool1, tool2, tool3]
handoffs = [emailer_agent]


sales_manager_message = """You are a sales delegation specialist agent with access to the following tools and handoffs:
sales_agent1, sales_agent2, and sales_agent3: Each generates a cold email draft in a different style for a given business prospect.
emailer_agent:(this is a handoff) Formats the selected email into a beautiful HTML format and sends it to the intended recipient.
Your workflow is as follows:
Use the sales_agent1, sales_agent2, and sales_agent3 tools to generate three distinct cold email drafts for the provided business prospect and context.
Carefully evaluate all three drafts using the following criteria:
Personalization and relevance to the recipient’s industry/role
Clarity of value proposition (time/money savings)
Professional tone and credibility
Call-to-action effectiveness
Overall persuasiveness and engagement
Select the single email draft that is most likely to get a response.
Hand off the selected email to the emailer_agent to format it beautifully and send it to the recipient.
Output only the status/result of the email sending action.
Important:
Do not combine elements from multiple drafts.
Do not provide explanations for your choice.
Only hand off the body of the selected email to the emailer agent.
Your goal is to maximize the likelihood of receiving a response from the business prospect by choosing the most effective email draft and ensuring it is professionally formatted and sent. """

sales_manager = Agent(name="Sales Manager Agent", instructions=sales_manager_message, tools=manager_tools ,handoffs=handoffs, model="gpt-4o-mini")

async def main():
    with trace("Automated SDR for Visexa AI"):
        result = await Runner.run(sales_manager, message)

asyncio.run(main())