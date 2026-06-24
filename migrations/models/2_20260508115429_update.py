from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "t_category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(64) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "t_user" ("id") ON DELETE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_t_category_created_fd8005" ON "t_category" ("created_at");
COMMENT ON COLUMN "t_category"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "t_category"."created_at" IS '创建时间';
COMMENT ON COLUMN "t_category"."updated_at" IS '更新时间';
COMMENT ON COLUMN "t_category"."name" IS '分类名称';
COMMENT ON COLUMN "t_category"."user_id" IS '用户';
COMMENT ON TABLE "t_category" IS '分类表';
        CREATE TABLE IF NOT EXISTS "t_article" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(128) NOT NULL,
    "intro" VARCHAR(256) NOT NULL,
    "content" TEXT NOT NULL,
    "view_count" INT NOT NULL DEFAULT 0,
    "seo_title" VARCHAR(256),
    "seo_keywords" VARCHAR(256),
    "seo_description" VARCHAR(1024),
    "category_id" INT NOT NULL REFERENCES "t_category" ("id") ON DELETE NO ACTION,
    "user_id" INT NOT NULL REFERENCES "t_user" ("id") ON DELETE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_t_article_created_c6a57d" ON "t_article" ("created_at");
COMMENT ON COLUMN "t_article"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "t_article"."created_at" IS '创建时间';
COMMENT ON COLUMN "t_article"."updated_at" IS '更新时间';
COMMENT ON COLUMN "t_article"."title" IS '文章标题';
COMMENT ON COLUMN "t_article"."intro" IS '文章摘要';
COMMENT ON COLUMN "t_article"."content" IS '文章内容';
COMMENT ON COLUMN "t_article"."view_count" IS '文章浏览量';
COMMENT ON COLUMN "t_article"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "t_article"."seo_keywords" IS 'SEO关键字';
COMMENT ON COLUMN "t_article"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "t_article"."category_id" IS '分类';
COMMENT ON COLUMN "t_article"."user_id" IS '用户';
COMMENT ON TABLE "t_article" IS '文章表';
        CREATE TABLE IF NOT EXISTS "t_tag" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(64) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "t_user" ("id") ON DELETE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_t_tag_created_719d35" ON "t_tag" ("created_at");
COMMENT ON COLUMN "t_tag"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "t_tag"."created_at" IS '创建时间';
COMMENT ON COLUMN "t_tag"."updated_at" IS '更新时间';
COMMENT ON COLUMN "t_tag"."name" IS '标签名称';
COMMENT ON COLUMN "t_tag"."user_id" IS '用户';
COMMENT ON TABLE "t_tag" IS '标签表';
        CREATE TABLE "t_article_tag" (
    "tag_id" INT NOT NULL REFERENCES "t_article" ("id") ON DELETE CASCADE,
    "article_id" INT NOT NULL REFERENCES "t_tag" ("id") ON DELETE NO ACTION
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "t_article_tag";
        DROP TABLE IF EXISTS "t_article";
        DROP TABLE IF EXISTS "t_tag";
        DROP TABLE IF EXISTS "t_category";"""


MODELS_STATE = (
    "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"
    "tm0Llpf1//iwZvk="
)
