def build_prompt(profile: dict, user_input: str) -> str:
    # Ambil info umum
    name = profile.get("name", "Asisten")
    role = profile.get("personality", {}).get("role", "")
    style = profile.get("personality", {}).get("style", "")
    languages = ", ".join(profile.get("personality", {}).get("language", []))

    # Aturan dan contoh
    rules = "\n".join(f"- {rule}" for rule in profile.get("rules", []))
    examples = "\n".join(f"- {example}" for example in profile.get("examples", []))

    # Fungsi yang tersedia
    functions = ", ".join(profile.get("functions", []))

    # Info author & sosial media
    author = profile.get("author", "")
    contact_author = profile.get("social_media_author", {})
    contact_info = "\n".join(
        f"- {key.title()}: {value}" for key, value in contact_author.items()
    )

    # Template prompt
    prompt_template = profile.get("prompt_template", "")

    return prompt_template.format(
        name=name,
        role=role,
        style=style,
        language=languages,
        author=author,
        social_media=contact_info,
        functions_call=functions,
        rules=rules,
        examples=examples,
        user_input=user_input
    )
