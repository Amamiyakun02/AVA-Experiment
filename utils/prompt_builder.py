def build_prompt(profile: dict, user_input: str) -> str:
    return profile["prompt_template"].format(
        name=profile["name"],
        role=profile["personality"]["role"],
        style=profile["personality"]["style"],
        language=", ".join(profile["personality"]["language"]),
        rules="\n".join(f"- {r}" for r in profile["rules"]),
        examples="\n".join(f"- {e}" for e in profile["examples"]),
        user_input=user_input
    )
