import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from typing import Optional
from config import Config
from platforms import get_platform
from storage import Storage

app = typer.Typer(help="Multi-platform social media posting CLI")
console = Console()
config = Config()
storage = Storage()

@app.command()
def post(
    message: str = typer.Argument(..., help="Message to post"),
    platforms: str = typer.Option("all", "--platforms", "-p", help="Comma-separated platform names or 'all'"),
    image: Optional[Path] = typer.Option(None, "--image", "-i", help="Image file path")
):
    """Post content to social media platforms"""
    platform_list = config.get_enabled_platforms() if platforms == "all" else platforms.split(",")
    
    results = []
    for platform_name in platform_list:
        try:
            platform = get_platform(platform_name, config)
            result = platform.post(message, image)
            results.append({"platform": platform_name, "status": "success", "result": result})
            console.print(f"[green]✓[/green] Posted to {platform_name}")
        except Exception as e:
            results.append({"platform": platform_name, "status": "failed", "error": str(e)})
            console.print(f"[red]✗[/red] Failed to post to {platform_name}: {e}")
    
    storage.save_post(message, results, image)

@app.command()
def history(limit: int = typer.Option(10, "--limit", "-n", help="Number of posts to show")):
    """Show posting history"""
    posts = storage.get_history(limit)
    
    if not posts:
        console.print("[yellow]No posting history found[/yellow]")
        return
    
    table = Table(title="Posting History")
    table.add_column("Time", style="cyan")
    table.add_column("Message", style="white")
    table.add_column("Platforms", style="green")
    table.add_column("Status", style="yellow")
    
    for post in posts:
        platforms_str = ", ".join([r["platform"] for r in post["results"]])
        success_count = sum(1 for r in post["results"] if r["status"] == "success")
        total_count = len(post["results"])
        status = f"{success_count}/{total_count}"
        
        table.add_row(
            post["timestamp"],
            post["message"][:50] + "..." if len(post["message"]) > 50 else post["message"],
            platforms_str,
            status
        )
    
    console.print(table)

@app.command()
def setup():
    """Setup configuration file"""
    env_path = Path(".env")
    example_path = Path(".env.example")
    
    if env_path.exists():
        console.print("[yellow]Configuration file already exists at .env[/yellow]")
        return
    
    if example_path.exists():
        import shutil
        shutil.copy(example_path, env_path)
        console.print("[green]Created .env from .env.example[/green]")
    else:
        with open(env_path, "w") as f:
            f.write("# Reddit\nREDDIT_CLIENT_ID=\nREDDIT_CLIENT_SECRET=\nREDDIT_USERNAME=\nREDDIT_PASSWORD=\n\n")
            f.write("# Discord\nDISCORD_WEBHOOK_URL=\n\n")
            f.write("# Telegram\nTELEGRAM_BOT_TOKEN=\nTELEGRAM_CHAT_ID=\n")
        console.print("[green]Created .env configuration file[/green]")
    
    console.print("\n[cyan]Please edit .env file with your API credentials[/cyan]")

if __name__ == "__main__":
    app()
