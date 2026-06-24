from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE "t_article_tag" (
    "t_article_id" INT NOT NULL REFERENCES "t_article" ("id") ON DELETE CASCADE,
    "tag_id" INT NOT NULL REFERENCES "t_tag" ("id") ON DELETE NO ACTION
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "t_article_tag";"""


MODELS_STATE = (
    "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"
    "tmB52fwPBm1onw=="
)
