from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "t_article" ADD "status" SMALLINT NOT NULL DEFAULT 0;
        COMMENT ON COLUMN "t_article"."status" IS '文章状态 0-未发布 1-已发布';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "t_article" DROP COLUMN "status";"""


MODELS_STATE = (
    "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"
)
