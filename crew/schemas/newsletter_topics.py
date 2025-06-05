from pydantic import BaseModel, Field
from typing import List

class Story(BaseModel):
    title: str = Field(..., description="Headline or title of the story")
    content: str = Field(..., description="Brief summary or content of the story")
    source: str = Field(..., description="URL of the original story")

class Tool(BaseModel):
    name: str = Field(..., description="Name of the featured AI tool")
    description: str = Field(..., description="What the tool does and why it's highlighted")
    link: str = Field(..., description="Link to access or learn more about the tool")

class QuoteOrTweet(BaseModel):
    content: str = Field(..., description="Interesting quote or tweet")
    source: str = Field(..., description="Source or attribution for the quote or tweet")

class NewsletterTopics(BaseModel):
    top_stories: List[Story] = Field(..., description="List of top AI news stories for the week")
    deep_dive: Story = Field(..., description="A single long-form analysis or spotlight story")
    tool_of_the_week: Tool = Field(..., description="Featured AI tool with details")
    quote_or_tweet: QuoteOrTweet = Field(..., description="Inspirational or thought-provoking quote or tweet")
    ai_in_the_wild: Story = Field(..., description="A real-world application of AI technology")
    hot_takes: Story = Field(..., description="Controversial or strong opinion in the AI space")
    editors_note: str = Field(..., description="A short editorial message or reflection from the editor")