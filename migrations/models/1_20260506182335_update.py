from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "t_user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(128) NOT NULL,
    "password" VARCHAR(128) NOT NULL,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_t_user_email_6fe6a5" ON "t_user" ("email");
CREATE INDEX IF NOT EXISTS "idx_t_user_created_9700b0" ON "t_user" ("created_at");
COMMENT ON COLUMN "t_user"."email" IS '邮箱';
COMMENT ON COLUMN "t_user"."password" IS '密码';
COMMENT ON COLUMN "t_user"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "t_user"."created_at" IS '创建时间';
COMMENT ON COLUMN "t_user"."updated_at" IS '更新时间';
COMMENT ON TABLE "t_user" IS '用户表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "t_user";"""


MODELS_STATE = (
    "eJztlm1vmzAQx79KxKtO6ipCA6F7l7SZmqlJppZuUx+EDJjEKtgUm7ZR1e++sxNCICFNJ/"
    "Vh2t5E4X935u53xr5HLWYBjvjeOcep9qXxqFEUY/hT0ncbGkqSQpWCQF6kHIWb5T4eFyny"
    "BaghijgGKcDcT0kiCKPS9yprm4Z9lVnGfvsqs23LlnEB8yGQ0DG40CyKQMoouc2wK9gYi4"
    "nK7PIaZEID/IB5/pjcuCHBUVBKnARyTaW7YpoorU/FV+Uo3+a5PouymBbOyVRMGF14Eyqk"
    "OsYUp0hgubxIM1mOzG5ed17hLNPCZZbiUkyAQ5RFoqitzCQXVxn4jEqekA1XBY7lWz4bzV"
    "a7Ze9bLRtcVCYLpf00K6+ofRaoCAwd7UnZkUAzD4Wx4IZjRKJVdIcTlK5ntwio4IOkq/hy"
    "WJv45cJLAcKmOtARhq3lec2a7VRFGaMHN8J0LCbw2DTsDeB+dE4PjzunO+D1Sa7OYIfPNv"
    "5wbjJmNkm3oJkgzu9ZumYv1gNdjnktpsWH+RxU0/MtgGrrHwcq4S4cP1jWv4K1y1iEEa35"
    "zEuBFbYeRL4W3Npz0LKMEBi3DGBsGoYOm9iyWtuR3gC2OxqdyEVizm8jJfSdCuDzQbcH5B"
    "V3cCICL58PBWw/xRKGi8Qq7COwCBLj9bTLkRXawTx0L//zxmeFaTQ9+AU/aIIZAv4DM9wS"
    "vAaFBSMaTecv3NAIpz/onTmdwfdSN446Tk9aDKVOK+qOVfkYFos0fvad44Z8bFyMhj2FlX"
    "ExTtUbCz/nQpM5oUwwl7J7FwVLbHI151fqdpYEf9jtcuTbdHv7U8yywpZstKf/w+1WycuB"
    "KbxZuvql4CH/5h6lgbtiYQar8101xUZcVRBFY9UryVZmOR8oOzgl/mTdqDm3bBw2UeHz3L"
    "BZP1j9Hy7ffLi8wymXKb1gGloKeedhaHuKpRHIMM0tRiDwqh2BlK18K8tP4wUQ5+5/J8Cm"
    "rm8zQ+p6/QwpbZWxhlGB6Zpb7tvZaFgzzxQhFZDnFAq8DIgvdhsR4eL6Y2LdQFFWXbqzcn"
    "g7g86vKtfDk1G3ehnJBbrA+F2vl6ffavpSTg=="
)
