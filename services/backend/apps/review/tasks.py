import json
from config.celery_app import celery_app
from db.session import SessionLocal
from registry.manager_registry import db_manager
from config.config import settings
import structlog

logger = structlog.get_logger()


@celery_app.task
def update_sentiment_and_tone(id: str):
    """Update sentiment and tone of the review based on review_id."""
    db = SessionLocal()
    model_manager = db_manager.get_manager("review")

    # Setup OpenAI client
    client = settings.openai.setup()

    try:
        # Fetch the review by review_id
        review = model_manager.get_review_by_id(db, id)
        if not review:
            logger.error(f"Review with review_id {id} not found.")
            return

        # If sentiment or tone is missing, calculate using LLM (OpenAI in this case)
        if not review.sentiment or not review.tone:
            logger.info(f"Updating sentiment and tone for review {id}.")

            # Construct the prompt for tone and sentiment prediction
            prompt = (
                "Analyze the sentiment and tone of the review based on the given text and star rating (1 to 10). "
                "Return a JSON response in the format: {'sentiment': '<replace_me>', 'tone': '<replace_me>'}."
            )

            content = {"text": review.text, "starts": review.stars}

            try:
                # Make OpenAI API request to analyze the tone and sentiment
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a helpful assistant. {prompt}",
                        },
                        {"role": "user", "content": json.dumps(content)},
                    ],
                )
                sentiment_tone = completion.choices[0].message.content
                sentiment_tone = json.loads(sentiment_tone)
                sentiment = sentiment_tone.get("sentiment")
                tone = sentiment_tone.get("tone")

                # Update the review with the sentiment and tone
                review.sentiment = sentiment
                review.tone = tone

                # Commit the changes to the database
                db.commit()
                db.refresh(review)
                logger.info(f"Successfully updated sentiment and tone for review {id}.")

            except Exception as e:
                logger.error(
                    f"Error while updating sentiment and tone for review {id}: {str(e)}"
                )
                db.rollback()

    finally:
        db.close()
