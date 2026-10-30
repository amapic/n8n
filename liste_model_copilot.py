import asyncio

from copilot import CopilotClient


async def main():
    async with CopilotClient() as client:
        models = await client.list_models()
        print(f"{len(models)} modèles disponibles :\n")
        for m in sorted(models, key=lambda x: x.id):
            state = m.policy.state if m.policy else "?"
            print(f"{m.id:<35} {m.name:<30} policy={state}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        print(f"Erreur : {type(exc).__name__}: {exc}")
