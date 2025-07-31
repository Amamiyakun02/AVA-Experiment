def build_prompt(profile: dict, user_input: str) -> str:
    return profile["prompt_template"].format(
        name=profile.get("name", "Asisten"),
        role=profile.get("personality", {}).get("role", ""),
        style=profile.get("personality", {}).get("style", ""),
        language=", ".join(profile.get("personality", {}).get("language", [])),
        rules="\n".join(f"- {rule}" for rule in profile.get("rules", [])),
        examples="\n".join(f"- {example}" for example in profile.get("examples", [])),
        user_input=user_input
    )
