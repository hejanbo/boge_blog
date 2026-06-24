from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "t_article_tag";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE "t_article_tag" (
    "article_id" INT NOT NULL REFERENCES "t_tag" ("id") ON DELETE CASCADE,
    "tag_id" INT NOT NULL REFERENCES "t_article" ("id") ON DELETE CASCADE
);"""


MODELS_STATE = (
    "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"
    "7unbbs62uZ2I1eYFxUNn3Jst/j/1sYPVw="
)
